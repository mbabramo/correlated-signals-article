"""Assemble audited exact-primary data and ready replay requests, without solving.

Inputs are explicit finished audit waves, never live production directories. Missing
cases remain visible. Numeric values and complete off-path strategies are retained.
Alternative truth maps and approximate profiles have separate catalogs and gates.
"""
import argparse
import json
import math
import pathlib

from article_release import ROOT, identity, read, save_new, utc, verify

MEASURES = (
    'MeritoriousPlaintiffShortfall', 'NonliableDefendantBurden',
    'LiableDefendantExcessBurden', 'GrossOutcomeError', 'RealLitigationExpenditures',
)


def close(a, b, label):
    if not math.isfinite(a) or not math.isfinite(b) or abs(a - b) > 1e-10:
        raise ValueError('Failed existing unrounded accounting tolerance: ' + label)


def validate_profile(audit, profile):
    if audit['Schema'] != 'validated-final-profile-v1' or audit['Passed'] is not True or audit['CompleteStrategyUnchanged'] is not True:
        raise ValueError('Expected a successful complete primary-profile audit')
    if audit['Case']['Id'] != audit['CaseId'] or profile['OptionSet'] != audit['OptionSetName'] or profile['AgreementEnabled'] is not True:
        raise ValueError('Profile identity or agreement contract differs')
    if len(audit['FullBestResponseGains']) != 2 or any(not math.isfinite(g) or abs(g) > 1e-7 for g in audit['FullBestResponseGains']):
        raise ValueError('Existing full primary best-response check did not pass')
    if len(profile['Strategies']) != audit['GameIdentity']['InformationSets']:
        raise ValueError('Complete information-set policy was not exported')
    if len({row['InformationSet'] for row in profile['Strategies']}) != len(profile['Strategies']):
        raise ValueError('Duplicate information sets')
    entries = 0
    agreement_reaches = [0.0, 0.0]
    for row in profile['Strategies']:
        probabilities = row['Probabilities']
        entries += len(probabilities)
        if len(probabilities) != len(row['Actions']) or any(not math.isfinite(p) or p < 0 or p > 1 for p in probabilities):
            raise ValueError('Invalid complete action vector')
        close(sum(probabilities), 1, 'complete strategy normalization')
        reach = row['Reach']
        if not math.isfinite(reach) or reach < 0 or reach > 1 + 1e-10:
            raise ValueError('Invalid joint reach')
        conditional = row['ReachedConditionalProbabilities']
        if (conditional is None) != (reach == 0):
            raise ValueError('Unreached conditionals must be undefined')
        if conditional is not None:
            if len(conditional) != len(probabilities):
                raise ValueError('Incomplete reached action vector')
            for a, b in zip(conditional, probabilities):
                close(a, b, 'reached conditional strategy')
        if row['Decision'] in ('PAgreeToBargain', 'DAgreeToBargain'):
            agreement_reaches[row['Player']] += reach
    if entries != audit['GameIdentity']['StrategyEntries']:
        raise ValueError('Missing action coordinates')
    close(agreement_reaches[0], agreement_reaches[1], 'joint agreement-stage reach')
    metrics = dict(profile['Metrics'], AgreementStageReach=agreement_reaches[0])
    agreement = [metrics[k] for k in ('BothAgreeGivenStage', 'OnlyPlaintiffDeclinesGivenStage',
                                     'OnlyDefendantDeclinesGivenStage', 'BothDeclineGivenStage')]
    if agreement_reaches[0] == 0:
        if any(value is not None for value in agreement):
            raise ValueError('Unreached agreement-stage conditionals are not zero observations')
    else:
        if any(value is None for value in agreement):
            raise ValueError('Reached agreement stage lacks joint outcomes')
        close(sum(agreement), 1, 'joint agreement outcomes')
    welfare = audit['Welfare']
    if set(welfare['Headline']) != set(MEASURES) or any(not math.isfinite(v) for v in welfare['Headline'].values()):
        raise ValueError('Expected all five unrounded welfare measures')
    close(welfare['TotalProbability'], 1, 'terminal probability')
    if welfare['MaximumAccountingResidual'] > 1e-10:
        raise ValueError('Existing monetary accounting failed')
    return metrics


def endpoint(audit):
    inputs = audit['Inputs']
    return dict(Case=audit['Case'], EquilibriumFile=inputs['Equilibrium']['Path'],
                ActionReportFile=inputs['Actions']['Path'], NumericReportFile=inputs['Numeric']['Path'],
                EquilibriumNumber=1)


def risk_label(case):
    p, d = case['AlphaP'], case['AlphaD']
    if p == d == 0:
        return 'Risk neutral'
    if p == d:
        return f'Symmetric risk aversion (alpha={p:g})'
    return f'Plaintiff alpha={p:g}; defendant alpha={d:g}'


def build(waves, output):
    output = pathlib.Path(output).resolve()
    if not output.is_relative_to(ROOT / 'reporting') or output == ROOT / 'reporting':
        raise ValueError('Keep catalogs in a fresh isolated reporting subdirectory')
    if output.exists():
        raise FileExistsError('Catalog snapshots are immutable; choose a fresh output directory')
    inventory_path = ROOT / 'planning' / 'Revised plan data' / 'equilibrium-inventory.plan.json'
    recipe_path = ROOT / 'production' / 'decomposition-requests.draft.json'
    expected = {c['case_id']: c for c in read(inventory_path)['cases']}
    recipes = read(recipe_path)
    if len(expected) != 82 or recipes['source_inventory_sha256'] != identity(inventory_path)['Sha256']:
        raise ValueError('Changed declared case/comparison matrix')
    audits, profiles, records = {}, {}, []
    wave_identities = []
    # Validate every file before writing any catalog output.
    for wave_path in waves:
        wave = read(wave_path)
        if wave.get('Passed') is not True or wave.get('SolvesStarted') != 0:
            raise ValueError('Only successful non-solving audit waves are accepted')
        verify(wave['Build'])
        verify(wave['Requests'])
        wave_identities.append(identity(wave_path))
        for audit_file in wave['Validated']:
            audit_path = verify(audit_file)
            audit = read(audit_path)
            case_id = audit['CaseId']
            if case_id not in expected or case_id in audits:
                raise ValueError('Unexpected or duplicate primary case: ' + case_id)
            for item in [audit['Request'], audit['GameAssembly'], audit['ReportingAssembly']]:
                verify(item)
            for item in audit['Inputs'].values():
                if isinstance(item, dict) and 'Path' in item and 'Sha256' in item:
                    verify(item)
            for item in audit['Outputs']:
                verify(item)
            profile_files = [item for item in audit['Outputs'] if pathlib.Path(item['Path']).parent.name == 'Profiles']
            if len(profile_files) != 1:
                raise ValueError('Expected one complete exported profile')
            profile = read(verify(profile_files[0]))
            metrics = validate_profile(audit, profile)
            for key, input_key in (('Profile', 'Equilibrium'), ('ActionReport', 'Actions')):
                if profile[key]['Sha256'].lower() != audit['Inputs'][input_key]['Sha256'].lower():
                    raise ValueError('Exported profile refers to another endpoint')
            case = audit['Case']
            planned = expected[case_id]
            if (case['FeeRule'], case['AlphaP'], case['AlphaD'], case['CostMultiplier']) != (
                    planned['fee_rule'], planned['alpha_p'], planned['alpha_d'], planned['cost_multiplier']):
                raise ValueError('Case labels differ from approved matrix')
            record = dict(CaseId=case_id, Parameters=case, RiskLabel=risk_label(case),
                          ComparisonFamily='baseline' if case['IsExternalImport'] else case['Family'],
                          Audit=audit_file, CompleteProfile=profile_files[0],
                          CompleteStrategySha256=audit['CompleteStrategySha256'],
                          Welfare=audit['Welfare'], ParticipationAndDispositions=metrics,
                          FullBestResponseGains=audit['FullBestResponseGains'],
                          PrimaryAcceptance='Original exact solve with complete-profile high-accuracy audit',
                          TruthMapping='Identity (baseline)', AlternativeTruthMapsIncluded=False)
            audits[case_id], profiles[case_id] = audit, profile
            records.append(record)
    comparisons, ready_requests, waiting = [], [], []
    for pair in recipes['welfare_rule_profile_pairs']:
        a, b = pair['american'], pair['complete']
        missing = [key for key in (a, b) if key not in audits]
        if missing:
            waiting.append(dict(**pair, MissingAuditedProfiles=missing))
            continue
        american, complete = audits[a], audits[b]
        if american['GameIdentity']['CoordinatesSha256'] != complete['GameIdentity']['CoordinatesSha256']:
            raise ValueError('Declared welfare pair has incompatible complete action coordinates')
        values_a, values_b = american['Welfare']['Headline'], complete['Welfare']['Headline']
        comparisons.append(dict(American=a, Complete=b, TruthMapping='Identity (baseline)',
                                AmericanLevels=values_a, CompleteLevels=values_b,
                                CompleteMinusAmerican={k: values_b[k] - values_a[k] for k in MEASURES},
                                DifferenceDefinition='Signed difference of unrounded established headline measures'))
        request = dict(Id=a + '--to--' + b, American=endpoint(american), Complete=endpoint(complete), TruthMapExponents=[1.0])
        ready_requests.append((request['Id'], request, [american['Request'], complete['Request']]))
    output.mkdir(parents=True, exist_ok=False)
    request_files = []
    for name, request, evidence in ready_requests:
        path = output / 'welfare-requests' / (name + '.json')
        save_new(path, request)
        request_files.append(dict(Request=identity(path), AuditedEndpoints=evidence, SolvesRequired=0))
    save_new(output / 'welfare-levels-and-differences.json', dict(
        Schema='audited-primary-welfare-v1', TruthMapping='Identity (baseline)', Measures=MEASURES,
        Cases=records, SignedFeeComparisons=comparisons, PendingFeeComparisons=waiting,
        HeadlineConvention='Configured truth-prior weighting of truth-conditional means; direct replay mass retained separately',
        DecompositionsStillRequired=True, AllPlannedCasesComplete=len(records) == len(expected)))
    save_new(output / 'ready-welfare-replays.json', dict(Schema='audited-welfare-replay-requests-v1',
        Requests=request_files, PlannedPairs=36, ReadyPairs=len(request_files), PendingPairs=waiting,
        Exponents=[1.0], AlternativeTruthSpecificationStillRequired=True, SolvesStarted=0))
    # Original 90 calculations remain import/reuse work owned by the original task.
    strategic = []
    for request in recipes['strategic_response']:
        missing = [key for key in (request['source'], request['target']) if key not in audits]
        strategic.append(dict(**request, MissingAuditedProfiles=missing,
                             Disposition='Reserve for original-calculation import' if 'inherited-current-90' in request['reasons']
                             else 'Ready to materialize from audited profiles' if not missing else 'Await audited endpoints'))
    save_new(output / 'strategic-coverage.json', dict(Schema='audited-strategic-coverage-v1',
        Contrasts=strategic, OriginalCalculationsReservedForReuse=90, PlannedDistinctContrasts=190, SolvesStarted=0))
    save_new(output / 'catalog.json', dict(Schema='audited-exact-primary-catalog-v1', CreatedUtc=utc(),
        DeclaredInventory=identity(inventory_path), ComparisonRecipes=identity(recipe_path), AuditWaves=wave_identities,
        Cases=records, ExpectedCases=82, AuditedCases=len(records),
        MissingAuditedCaseIds=sorted(set(expected) - set(audits)), Complete=len(records) == 82,
        Generator=identity(__file__), SolvesStarted=0,
        Outputs=[identity(p) for p in sorted(output.rglob('*')) if p.is_file()]))
    return dict(AuditedCases=len(records), ExpectedCases=82, ReadyWelfarePairs=len(ready_requests),
                PendingWelfarePairs=len(waiting), Output=str(output), SolvesStarted=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wave', action='append', required=True, type=pathlib.Path)
    parser.add_argument('--output', required=True, type=pathlib.Path)
    args = parser.parse_args()
    print(json.dumps(build(args.wave, args.output), indent=2))
