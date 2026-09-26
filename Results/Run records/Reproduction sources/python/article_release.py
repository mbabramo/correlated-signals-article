"""Explicit, archived, file-by-file publication of the validated article collection.

Preparation never writes to the article repository. Application requires a complete
release certificate, a byte-verified archive and a fully classified change manifest.
There is deliberately no recursive removal, git operation or automatic recovery.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import shutil
import stat
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARTICLE = pathlib.Path(r'C:\Users\Admin\source\repos\correlated-signals-article')
SCOPES = (
    'Results/Aggregated Data', 'Results/Individual simulations',
    'Results/Truth mapping sensitivity', 'Results/Run records',
    'Supplemental materials/Generated pairwise comparisons',
    'Supplemental materials/Equilibrium strategy changes',
    'Supplemental materials/Welfare decompositions', 'Supplemental materials/Welfare overview',
    'Supplemental materials/Multiple equilibria', 'Supplemental materials/Equilibrium solution paths',
    'Supplemental materials/Game tree diagrams', 'Supplemental materials/Liability signals diagrams',
)
PROTECTED_SCOPES = ('Figures', 'Tables', 'Supplemental materials/Risk aversion utility curves')
RELEASE_GATES = (
    'ExactECTAAdoption', 'PrimaryProfiles', 'OriginalImports', 'TruthMappings',
    'ApproximateCatalogs', 'WelfareCoverage', 'WelfareDecompositions',
    'StrategicDecompositions', 'TrajectoryReplays', 'ExhibitInventory',
    'StaticVisualQA', 'InteractiveVisualQA', 'FindingsAndIndexes', 'ProtectedContent',
)


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    digest = hashlib.sha256()
    with pathlib.Path(path).open('rb') as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def identity(path):
    path = pathlib.Path(path).resolve()
    return dict(Path=str(path), Sha256=sha(path), Bytes=path.stat().st_size)


def verify(item):
    path = pathlib.Path(item['Path'])
    if sha(path).lower() != item['Sha256'].lower():
        raise ValueError('Changed frozen file: ' + str(path))
    return path


def save_new(path, value):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as file:
        json.dump(value, file, indent=2, allow_nan=False)
        file.write('\n')
        file.flush()
        os.fsync(file.fileno())


def relative(value):
    """Reject Windows aliases/ADS/traversal even when tested on another platform."""
    if not isinstance(value, str) or not value or '\\' in value:
        raise ValueError('Use a nonempty slash-separated relative path')
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or str(path) != value:
        raise ValueError('Path must be canonical and relative: ' + value)
    reserved = {'con', 'prn', 'aux', 'nul', *(f'com{i}' for i in range(1, 10)), *(f'lpt{i}' for i in range(1, 10))}
    for part in path.parts:
        if part in ('.', '..') or part.endswith((' ', '.')) or any(c in part for c in ':<>"|?*') or any(ord(c) < 32 for c in part):
            raise ValueError('Unsafe path component: ' + value)
        if part.split('.')[0].lower() in reserved:
            raise ValueError('Reserved device path: ' + value)
    return path


def permitted(value):
    rel = str(relative(value)).casefold()
    return rel == 'readme.md' or any(rel.startswith(scope.casefold() + '/') for scope in SCOPES)


def is_link(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def contained(root, value):
    root = pathlib.Path(root).resolve()
    rel = relative(value)
    current = root
    for part in rel.parts:
        current = current / part
        if current.exists() or current.is_symlink():
            if is_link(current):
                raise ValueError('Links and junctions are not publication targets: ' + str(current))
    if not current.resolve().is_relative_to(root):
        raise ValueError('Path leaves the declared root')
    return current


def inventory(root, scopes=SCOPES, include_readme=True):
    root = pathlib.Path(root).resolve()
    files = {}
    candidates = []
    if include_readme and (root / 'README.md').is_file():
        candidates.append(root / 'README.md')
    for scope in scopes:
        directory = contained(root, scope)
        if not directory.exists():
            continue
        if not directory.is_dir():
            raise ValueError('Expected directory: ' + str(directory))
        # os.walk never follows links; reject them, including directory junctions.
        for parent, directories, names in os.walk(directory, followlinks=False):
            for name in directories + names:
                item = pathlib.Path(parent) / name
                if is_link(item):
                    raise ValueError('Archive scope contains a link: ' + str(item))
            candidates.extend(pathlib.Path(parent) / name for name in names)
    for item in sorted(candidates):
        rel = item.relative_to(root).as_posix()
        contained(root, rel)
        if rel.casefold() in files:
            raise ValueError('Case-insensitive file collision: ' + rel)
        files[rel.casefold()] = dict(RelativePath=rel, Sha256=sha(item), Bytes=item.stat().st_size)
    return files


def independent_roots(article, stage, archive):
    roots = [pathlib.Path(p).resolve() for p in (article, stage, archive)]
    for i, a in enumerate(roots):
        for b in roots[i + 1:]:
            if a == b or a.is_relative_to(b) or b.is_relative_to(a):
                raise ValueError('Article, staging and archive roots must be separate')
    return roots


def prepare(article, stage, archive, decisions, output):
    article, stage, archive = independent_roots(article, stage, archive)
    if not stage.is_dir() or not article.is_dir() or archive.exists():
        raise ValueError('Require existing article/stage and a fresh archive directory')
    old = inventory(article)
    new = inventory(stage)
    all_stage = inventory(stage, tuple(p.name for p in stage.iterdir() if p.is_dir()))
    if set(all_stage) != set(new):
        raise ValueError('Staged directory contains files outside permitted generated scopes')
    if any(p.is_file() and p.name != 'README.md' for p in stage.iterdir()):
        raise ValueError('Place release metadata outside the staged article tree')
    decisions_by_path = {}
    for decision in decisions:
        key = str(relative(decision['RelativePath'])).casefold()
        if key in decisions_by_path or key not in old or key in new:
            raise ValueError('Disposition must uniquely address an old file absent from staging')
        if decision['Action'] not in ('Retain', 'Remove') or not decision.get('Reason', '').strip():
            raise ValueError('Explicit retain/remove reason required')
        decisions_by_path[key] = decision
    actions = []
    for key in sorted(set(old) | set(new)):
        before, after = old.get(key), new.get(key)
        rel = (before or after)['RelativePath']
        if after and before and after['RelativePath'] != before['RelativePath']:
            raise ValueError('Case-only renaming needs separate review: ' + rel)
        if not permitted(rel):
            raise ValueError('Protected or unrelated target: ' + rel)
        if after:
            action = 'Add' if not before else 'Retain' if before['Sha256'] == after['Sha256'] else 'Replace'
            reason = 'Validated staged generated file' if action != 'Retain' else 'Staged and existing bytes are identical'
        else:
            decision = decisions_by_path.get(key)
            action = decision['Action'] if decision else 'Unresolved'
            reason = decision['Reason'] if decision else 'Preserve pending file-level classification; application is blocked'
        actions.append(dict(RelativePath=rel, Action=action, Reason=reason,
                            OldSha256=before['Sha256'] if before else None,
                            NewSha256=after['Sha256'] if after else None))
    protected = inventory(article, PROTECTED_SCOPES, include_readme=False)
    plan = dict(Schema='explicit-article-publication-v1', CreatedUtc=utc(),
                ArticleRoot=str(article), StageRoot=str(stage), ArchiveRoot=str(archive),
                OldFiles=list(old.values()), StagedFiles=list(new.values()),
                ProtectedFiles=list(protected.values()), Actions=actions,
                ReadyForArchive=not any(a['Action'] == 'Unresolved' for a in actions),
                Script=identity(__file__), UserRepositoriesModified=False)
    save_new(output, plan)
    return plan


def check_plan(plan):
    if plan['Schema'] != 'explicit-article-publication-v1' or not plan['ReadyForArchive']:
        raise ValueError('Unresolved or unrecognized publication plan')
    roots = independent_roots(plan['ArticleRoot'], plan['StageRoot'], plan['ArchiveRoot'])
    seen = set()
    for item in plan['Actions']:
        rel = item['RelativePath']
        if not permitted(rel) or rel.casefold() in seen or not item['Reason'].strip():
            raise ValueError('Unsafe or duplicate action')
        seen.add(rel.casefold())
        if item['Action'] not in ('Retain', 'Remove', 'Replace', 'Add'):
            raise ValueError('Unresolved action')
        if (item['Action'] in ('Remove', 'Replace', 'Retain')) != (item['OldSha256'] is not None):
            raise ValueError('Invalid old-file identity')
        if item['Action'] in ('Add', 'Replace') and item['NewSha256'] is None:
            raise ValueError('Missing staged identity')
        for root in roots[:2]:
            contained(root, rel)
    old = {i['RelativePath'].casefold(): i['Sha256'] for i in plan['OldFiles']}
    new = {i['RelativePath'].casefold(): i['Sha256'] for i in plan['StagedFiles']}
    if seen != set(old) | set(new) or len(old) != len(plan['OldFiles']) or len(new) != len(plan['StagedFiles']):
        raise ValueError('Action inventory is incomplete or ambiguous')
    for action in plan['Actions']:
        key = action['RelativePath'].casefold()
        if action['OldSha256'] != old.get(key) or action['NewSha256'] != new.get(key):
            raise ValueError('Action hash differs from collection inventory')
        if action['Action'] == 'Remove' and key in new:
            raise ValueError('Cannot remove a staged file')
        if action['Action'] == 'Retain' and key in new and old[key] != new[key]:
            raise ValueError('Retain would omit changed staged bytes')
    return roots


def matches_inventory(root, expected, protected=False):
    actual = inventory(root, PROTECTED_SCOPES if protected else SCOPES, include_readme=not protected)
    if actual != {i['RelativePath'].casefold(): i for i in expected}:
        raise ValueError('Collection changed after planning: ' + str(root))


def archive_plan(plan_path):
    plan = read(plan_path)
    article, stage, archive = check_plan(plan)
    matches_inventory(article, plan['OldFiles'])
    matches_inventory(stage, plan['StagedFiles'])
    matches_inventory(article, plan['ProtectedFiles'], protected=True)
    archive.mkdir(parents=True, exist_ok=False)
    records = []
    for item in plan['OldFiles'] + plan['ProtectedFiles']:
        rel = item['RelativePath']
        source, target = contained(article, rel), contained(archive / 'files', rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if sha(source) != item['Sha256'] or sha(target) != item['Sha256']:
            raise ValueError('Archive copy changed during preservation: ' + rel)
        records.append(dict(**item, ArchivePath=str(target)))
    # A source added during copying must not escape archival coverage.
    matches_inventory(article, plan['OldFiles'])
    matches_inventory(article, plan['ProtectedFiles'], protected=True)
    save_new(archive / 'archive-manifest.json', dict(Schema='verified-article-archive-v1',
        Passed=True, FinishedUtc=utc(), Plan=identity(plan_path), Files=records))
    save_new(archive / 'rollback-instructions.json', dict(
        Schema='explicit-article-rollback-instructions-v1', Plan=identity(plan_path),
        AutomaticRollbackAllowed=False,
        Procedure=[
            'Read application-journal.jsonl before any recovery. Retain intent records interrupted before Applied.',
            'For each applied replacement/removal, verify the archived old hash and the current target state first.',
            'Restore archived bytes only when the target still has the published hash or is absent after a logged removal.',
            'Remove a published addition only if its current bytes still match the new hash.',
            'A target with any other bytes may contain later user edits: preserve it and investigate.',
            'Use individual literal file operations. Do not recursively delete or restore the article tree.',
            'Recheck every protected file and record each actual restoration.'
        ], Actions=[dict(RelativePath=a['RelativePath'], PublicationAction=a['Action'],
                         PublishedSha256=a['NewSha256'], ArchivedSha256=a['OldSha256'],
                         ArchivePath=str(contained(archive / 'files', a['RelativePath'])) if a['OldSha256'] else None)
                    for a in plan['Actions'] if a['Action'] != 'Retain']))
    return archive / 'archive-manifest.json'


def visual_review_assets(evidence):
    """Read actual review assertions; an evidence-file hash alone is not approval."""
    review = read(verify(evidence))
    if review.get('Passed') is not True:
        raise ValueError('Visual evidence records a pending or failed review')
    method = review.get('InspectionMethod', review.get('Method'))
    if not isinstance(method, str) or not method.strip():
        raise ValueError('Visual evidence lacks its actual inspection method')
    schema = review.get('Schema')
    if schema == 'interactive-trajectory-visual-qa-v1':
        for key in ('InteractiveVisualQAPassed', 'PlaybackPassed', 'SteppingPassed', 'EndpointsPassed'):
            if review.get(key) is not True:
                raise ValueError('Interactive inspection is incomplete: ' + key)
        assets = review.get('Files', [])
        extensions = {'.html'}
    elif schema in ('page-by-page-visual-qa-v1', 'final-signal-visual-review-v1',
                    'final-structure-visual-qa-v1', 'model-worked-path-visual-qa-v1'):
        extensions = {'.pdf', '.png'}
        assets = []
        groups = review.get('Artifacts', [review])
        if not isinstance(groups, list) or not groups:
            raise ValueError('Visual evidence lacks reviewed artifacts')
        for group in groups:
            pdfs = group.get('PDFs', [group['PDF']] if 'PDF' in group else [])
            pages = group.get('Pages', [])
            if not pdfs or not pages:
                raise ValueError('Static review requires both PDF and inspected pages')
            if any(pathlib.Path(f['Path']).suffix.lower() != '.pdf' for f in pdfs):
                raise ValueError('Static PDF identity has the wrong file type')
            if any(pathlib.Path(f['Path']).suffix.lower() != '.png' for f in pages):
                raise ValueError('Static page identity has the wrong file type')
            assets.extend([*pdfs, *pages])
    else:
        raise ValueError('Unrecognized actual visual-review evidence schema')
    if not isinstance(assets, list) or not assets:
        raise ValueError('Visual evidence contains no inspected files')
    paths = set()
    for item in assets:
        path = verify(item)
        key = str(path.resolve()).casefold()
        if key in paths or path.suffix.lower() not in extensions:
            raise ValueError('Duplicate reviewed file or incorrect review type')
        paths.add(key)
    return dict(Method=method, Assets=assets)


def validate_certificate(certificate_path, plan_path, expected_cases):
    certificate = read(certificate_path)
    if certificate.get('Schema') != 'validated-article-release-v1' or certificate.get('Passed') is not True:
        raise ValueError('The complete validated-delivery certificate is required')
    if verify(certificate['PublicationPlan']).resolve() != pathlib.Path(plan_path).resolve():
        raise ValueError('Release certificate binds another publication plan')
    actual_cases = certificate['PrimaryCaseIds']
    if (not isinstance(actual_cases, list) or not isinstance(expected_cases, list)
            or any(not isinstance(c, str) or not c.strip() for c in actual_cases + expected_cases)
            or len(expected_cases) != 82 or len(set(expected_cases)) != 82
            or len(actual_cases) != 82 or len(set(actual_cases)) != 82
            or sorted(actual_cases) != sorted(expected_cases)):
        raise ValueError('The complete declared 82-case matrix is required')
    gates = certificate['Gates']
    if set(gates) != set(RELEASE_GATES):
        raise ValueError('Missing required article release evidence')
    for name, gate in gates.items():
        if gate.get('Passed') is not True or not gate.get('Evidence'):
            raise ValueError('Article release gate has not passed: ' + name)
        for file in gate['Evidence']:
            verify(file)
    plan = read(plan_path)
    staged_visuals = {i['RelativePath'].casefold(): i for i in plan['StagedFiles']
                      if pathlib.PurePosixPath(i['RelativePath']).suffix.lower() in ('.pdf', '.png', '.html')}
    reviews = {}
    for item in certificate['VisualReviews']:
        key = str(relative(item['RelativePath'])).casefold()
        if key in reviews:
            raise ValueError('Duplicate release visual review')
        reviews[key] = item
    if set(reviews) != set(staged_visuals):
        raise ValueError('Visual reviews must cover exactly the staged PDF/PNG/HTML files')
    checked_reviews = {}
    for key, item in staged_visuals.items():
        review = reviews[key]
        if review.get('Passed') is not True or review['Sha256'] != item['Sha256']:
            raise ValueError('Missing current visual/playback review: ' + item['RelativePath'])
        evidence = review['Evidence']
        identity_key = (str(pathlib.Path(evidence['Path']).resolve()).casefold(), evidence['Sha256'].lower())
        if identity_key not in checked_reviews:
            checked_reviews[identity_key] = visual_review_assets(evidence)
        actual = checked_reviews[identity_key]
        suffix = pathlib.PurePosixPath(item['RelativePath']).suffix.lower()
        if review.get('Method') != actual['Method'] or not any(
                f['Sha256'].lower() == item['Sha256'].lower()
                and pathlib.Path(f['Path']).suffix.lower() == suffix for f in actual['Assets']):
            raise ValueError('Evidence does not approve this staged artifact: ' + item['RelativePath'])
    return certificate


def append_event(path, event):
    with pathlib.Path(path).open('a', encoding='utf-8', newline='\n') as file:
        file.write(json.dumps(dict(Utc=utc(), **event), allow_nan=False) + '\n')
        file.flush()
        os.fsync(file.fileno())


def atomic_copy(source, target, expected):
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + '.article-release-pending')
    # Never overwrite a previous operation's incomplete payload.
    with source.open('rb') as src, temporary.open('xb') as dst:
        shutil.copyfileobj(src, dst, 1024 * 1024)
        dst.flush()
        os.fsync(dst.fileno())
    if sha(temporary) != expected:
        raise ValueError('Replacement bytes changed before application')
    os.replace(temporary, target)


def apply_plan(plan_path, certificate_path, expected_cases):
    plan = read(plan_path)
    article, stage, archive = check_plan(plan)
    validate_certificate(certificate_path, plan_path, expected_cases)
    backup = read(archive / 'archive-manifest.json')
    if backup['Schema'] != 'verified-article-archive-v1' or backup['Passed'] is not True or verify(backup['Plan']).resolve() != pathlib.Path(plan_path).resolve():
        raise ValueError('Missing verified archive of this plan')
    expected_backup = {i['RelativePath']: i['Sha256'] for i in plan['OldFiles'] + plan['ProtectedFiles']}
    if {i['RelativePath']: i['Sha256'] for i in backup['Files']} != expected_backup:
        raise ValueError('Archive lacks full prior generated/protected collection')
    for item in backup['Files']:
        path = contained(archive / 'files', item['RelativePath'])
        if sha(path) != item['Sha256']:
            raise ValueError('Archived source changed')
    matches_inventory(article, plan['OldFiles'])
    matches_inventory(stage, plan['StagedFiles'])
    matches_inventory(article, plan['ProtectedFiles'], protected=True)
    save_new(archive / 'application-started.json', dict(StartedUtc=utc(), Plan=identity(plan_path),
        Certificate=identity(certificate_path), Pid=os.getpid(), AutomaticRetryAllowed=False))
    journal = archive / 'application-journal.jsonl'
    for action in plan['Actions']:
        rel, kind = action['RelativePath'], action['Action']
        if kind == 'Retain':
            continue
        target, source = contained(article, rel), contained(stage, rel)
        if kind == 'Add':
            if target.exists():
                raise ValueError('New target appeared during publication: ' + rel)
        elif sha(target) != action['OldSha256']:
            raise ValueError('Existing target changed during publication: ' + rel)
        if kind != 'Add' and sha(contained(archive / 'files', rel)) != action['OldSha256']:
            raise ValueError('Archive changed before mutation')
        if kind in ('Replace', 'Add') and sha(source) != action['NewSha256']:
            raise ValueError('Staged replacement changed before mutation')
        append_event(journal, dict(State='Intent', **action))
        if kind == 'Remove':
            target.unlink()  # One verified literal file; never recursive deletion.
        else:
            atomic_copy(source, target, action['NewSha256'])
        append_event(journal, dict(State='Applied', **action))
    expected = {i['RelativePath'].casefold(): i for i in plan['StagedFiles']}
    old = {i['RelativePath'].casefold(): i for i in plan['OldFiles']}
    for action in plan['Actions']:
        if action['Action'] == 'Retain' and action['NewSha256'] is None:
            expected[action['RelativePath'].casefold()] = old[action['RelativePath'].casefold()]
    matches_inventory(article, list(expected.values()))
    matches_inventory(article, plan['ProtectedFiles'], protected=True)
    save_new(archive / 'application-result.json', dict(Passed=True, FinishedUtc=utc(),
        Plan=identity(plan_path), Certificate=identity(certificate_path),
        ProtectedCollectionUnchanged=True, ActionsApplied=sum(a['Action'] != 'Retain' for a in plan['Actions'])))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    prepare_parser = sub.add_parser('prepare')
    prepare_parser.add_argument('--stage', required=True, type=pathlib.Path)
    prepare_parser.add_argument('--archive', required=True, type=pathlib.Path)
    prepare_parser.add_argument('--decisions', required=True, type=pathlib.Path)
    prepare_parser.add_argument('--output', required=True, type=pathlib.Path)
    for mode in ('archive', 'apply'):
        command = sub.add_parser(mode)
        command.add_argument('--plan', required=True, type=pathlib.Path)
        if mode == 'apply':
            command.add_argument('--certificate', required=True, type=pathlib.Path)
    args = parser.parse_args()
    if args.mode == 'prepare':
        if not args.stage.resolve().is_relative_to(ROOT / 'article-staging') or not args.archive.resolve().is_relative_to(ROOT / 'archive'):
            raise ValueError('Use isolated article-staging and archive subdirectories')
        if not args.output.resolve().is_relative_to(ROOT / 'provenance'):
            raise ValueError('Keep publication plans in isolated provenance')
        plan = prepare(ARTICLE, args.stage, args.archive, read(args.decisions), args.output)
        print(json.dumps(dict(ReadyForArchive=plan['ReadyForArchive'], Actions=len(plan['Actions']), ArticleModified=False)))
    else:
        plan = read(args.plan)
        if pathlib.Path(plan['ArticleRoot']).resolve() != ARTICLE.resolve():
            raise ValueError('Unexpected article root')
        if not pathlib.Path(plan['StageRoot']).resolve().is_relative_to(ROOT / 'article-staging') or not pathlib.Path(plan['ArchiveRoot']).resolve().is_relative_to(ROOT / 'archive'):
            raise ValueError('Unexpected isolated staging/archive root')
        if args.mode == 'archive':
            print(archive_plan(args.plan))
        else:
            cases = read(ROOT / 'planning' / 'Revised plan data' / 'equilibrium-inventory.plan.json')['cases']
            protected = read(ROOT / 'planning' / 'Revised plan data' / 'protected-file-baseline.json')['files']
            for item in protected:
                verify(dict(Path=item['path'], Sha256=item['sha256']))
            apply_plan(args.plan, args.certificate, [c['case_id'] for c in cases])
            for item in protected:
                verify(dict(Path=item['path'], Sha256=item['sha256']))
            print('Completed explicit publication and protected-content verification')


if __name__ == '__main__':
    main()
