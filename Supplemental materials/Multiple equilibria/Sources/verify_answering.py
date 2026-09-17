"""Check the answering finding directly against saved per-signal action reports."""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def verify(root):
    root = root.resolve()
    summary = root / 'Sources/equilibrium-outcomes.csv'
    with summary.open(encoding='utf-8-sig', newline='') as stream:
        outcomes = list(csv.DictReader(stream))
    fingerprints = {}

    def source(path):
        relative = path.relative_to(root).as_posix()
        fingerprints[relative] = hashlib.sha256(path.read_bytes()).hexdigest().upper()

    source(summary)
    records = []
    grouped = defaultdict(list)
    for outcome in outcomes:
        path = root / 'Sources/Production' / outcome['Source File'].replace('.csv', '-InformationSetActions.csv')
        with path.open(encoding='utf-8-sig', newline='') as stream:
            answers = [row for row in csv.DictReader(stream)
                       if row['Decision'] == 'D Answers' and row['Action Label'] == 'Yes']
        assert len(answers) == 10, (path, len(answers))
        probabilities = [float(row['Equilibrium Action Probability']) for row in answers]
        reached = [float(row['Equilibrium Action Probability']) for row in answers
                   if row['Off Path'].lower() == 'false']
        assert reached, path
        universal = all(abs(p - 1) <= 1e-12 for p in reached)
        nonanswer = float(outcome['Does Not Answer'])
        assert universal == (abs(nonanswer) <= 1e-12), (path, probabilities, nonanswer)
        if outcome['Fee Rule'] == 'Complete Fee-Shifting':
            assert len(reached) == 10 and all(abs(p - 1) <= 1e-12 for p in probabilities), path
            assert abs(float(outcome['D Answers']) - float(outcome['P Files'])) <= 1e-6, path
        record = {
            'Risk': outcome['Risk Aversion'], 'FeeRule': outcome['Fee Rule'],
            'Equilibrium': int(outcome['Equilibrium']),
            'AnswerInformationSets': len(answers), 'ReachedAnswerInformationSets': len(reached),
            'MinimumAnswerProbabilityAtReachedInformationSets': min(reached),
            'UniversalAnsweringAfterFiling': universal,
            'UnconditionalNonanswerShare': nonanswer,
            'ActionReport': path.relative_to(root).as_posix(),
        }
        records.append(record)
        grouped[outcome['Risk Aversion'], outcome['Fee Rule']].append(record)
        source(path)

    groups = []
    for (risk, fee), profiles in grouped.items():
        groups.append({
            'Risk': risk, 'FeeRule': fee, 'Profiles': len(profiles),
            'ProfilesWithUniversalAnswering': sum(p['UniversalAnsweringAfterFiling'] for p in profiles),
            'MinimumUnconditionalNonanswerShare': min(p['UnconditionalNonanswerShare'] for p in profiles),
            'MaximumUnconditionalNonanswerShare': max(p['UnconditionalNonanswerShare'] for p in profiles),
        })
    complete = [p for p in records if p['FeeRule'] == 'Complete Fee-Shifting']
    trial_neutral = grouped['Risk Neutral', 'Trial Fee-Shifting']
    trial_averse = grouped['Moderately Risk Averse', 'Trial Fee-Shifting']
    assert len(complete) == 22 and sum(p['UniversalAnsweringAfterFiling'] for p in complete) == 22
    assert sum(p['UniversalAnsweringAfterFiling'] for p in trial_neutral) == 0
    assert [p['Equilibrium'] for p in trial_averse if p['UniversalAnsweringAfterFiling']] == [16]
    result = {
        'VerifiedUtc': datetime.now(timezone.utc).isoformat(), 'Status': 'Passed',
        'Scope': 'Six ordinary-cost, ten-offer cases; risk neutrality and symmetric CARA alpha 2.',
        'Method': 'Compare reported nonanswer shares with all reached defendant-answer information sets. For Complete Fee-Shifting, also require answering probability one at all ten signals in every profile and unconditional answering share equal to filing share.',
        'Interpretation': 'Universal answering means defendants answer whenever a suit is filed. It does not mean that all potential disputes are filed or answered. This verifies the recovered profiles, not all possible equilibria or other parameter specifications.',
        'CompleteFeeShiftingProfiles': 22, 'CompleteFeeShiftingAnswerInformationSets': 220,
        'Groups': groups, 'Profiles': records,
        'Sources': [{'Path': path, 'Sha256': digest} for path, digest in sorted(fingerprints.items())],
    }
    destination = root / 'Sources/answering-verification.json'
    destination.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({key: result[key] for key in ['Status', 'CompleteFeeShiftingProfiles',
                     'CompleteFeeShiftingAnswerInformationSets', 'Groups']}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parent.parent)
    verify(parser.parse_args().root)
