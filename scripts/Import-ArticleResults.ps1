param(
    [string]$ResultsSource = 'C:\Users\Admin\Documents\GitHub\ACESim4\ReportResults',
    [string]$Python = 'C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
)
$ErrorActionPreference = 'Stop'
$article = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$source = (Resolve-Path -LiteralPath $ResultsSource).Path
$inventory = Get-Content -LiteralPath (Join-Path $source 'Run records\diagram-inventory.json') -Raw | ConvertFrom-Json
if (!$inventory.Compiled -or $inventory.Cases -ne 124 -or $inventory.Artifacts.Count -ne 937) {
    throw 'Only the completed, verified 124-case/937-exhibit collection may be imported.'
}
foreach ($artifact in $inventory.Artifacts) {
    $sourceFile = [IO.Path]::GetFullPath($artifact.Source)
    if (!$sourceFile.StartsWith($source + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Unexpected source artifact path.' }
    $parent = Split-Path -Parent (Split-Path -Parent $sourceFile)
    $stem = [IO.Path]::GetFileNameWithoutExtension($sourceFile)
    foreach ($ext in @('.pdf','.png')) {
        if (!(Test-Path -LiteralPath (Join-Path $parent ($stem+$ext)))) { throw "Missing rendered artifact: $stem$ext" }
    }
}
function Assert-ArticleChild([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path)
    if (!$full.StartsWith($article + '\', [StringComparison]::OrdinalIgnoreCase)) { throw "Outside article: $full" }
    if (Test-Path -LiteralPath $full) {
        $item = Get-Item -LiteralPath $full
        if ($item.Attributes.HasFlag([IO.FileAttributes]::ReparsePoint)) { throw "Reparse point: $full" }
        if ((Resolve-Path -LiteralPath $full).Path -ne $full) { throw "Unexpected resolved target: $full" }
    }
    return $full
}
function Move-ArticleFolder([string]$Old,[string]$New) {
    $from = Assert-ArticleChild (Join-Path $article $Old)
    $to = Assert-ArticleChild (Join-Path $article $New)
    if (!(Test-Path -LiteralPath $from)) { return }
    if (Test-Path -LiteralPath $to) { throw "Destination already exists: $to" }
    New-Item -ItemType Directory -Path (Split-Path -Parent $to) -Force | Out-Null
    Move-Item -LiteralPath $from -Destination $to
}
if (Test-Path -LiteralPath (Join-Path $article 'Results\Equilibrium diagnostics')) {
    & $Python (Join-Path $PSScriptRoot 'relocate_supplemental.py') capture
    if ($LASTEXITCODE -ne 0) { throw 'Failed to preserve separate analysis inputs.' }
    Move-ArticleFolder 'Results\Equilibrium diagnostics' 'Supplemental materials\Equilibrium strategy changes\Calculations'
    Move-ArticleFolder 'Tables\Equilibrium strategy changes' 'Supplemental materials\Equilibrium strategy changes\Tables'
    Move-ArticleFolder 'Supplemental materials\Fee shifting on exit\Equilibrium strategy changes' 'Supplemental materials\Equilibrium strategy changes\Fee trigger comparison'
}
& $Python (Join-Path $PSScriptRoot 'relocate_supplemental.py') rebase
if ($LASTEXITCODE -ne 0) { throw 'Failed to rebase separate workflows; Results was not replaced.' }
foreach ($relative in @('Supplemental materials\Participation restrictions','Supplemental materials\Cost comparisons',
    'Supplemental materials\Risk aversion','Supplemental materials\Fee shifting on exit','Results','Figures','Tables',
    'publication-figures.json','publication-tables.json')) {
    $target = Assert-ArticleChild (Join-Path $article $relative)
    if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
}
Copy-Item -LiteralPath $source -Destination (Join-Path $article 'Results') -Recurse
foreach ($name in @('Figures','Tables')) { New-Item -ItemType Directory -Path (Join-Path $article $name) | Out-Null }
$config = [ordered]@{
    UseArticleResultsLayout=$true;WelfareExhibitsRequest='Results/welfare-exhibits.json';MaxParallelCompilers=[Environment]::ProcessorCount;
    ProcessTimeoutSeconds=300;LatexExecutable='lualatex';PreviewExecutable='pdftoppm';
    GameTreesDirectory='Supplemental materials/Game tree diagrams';SignalsDirectory='Supplemental materials/Liability signals diagrams';
    SignalSpecifications=@('Baseline','TruthConditionedLatentMerits','DirectBinaryStateSignals');
    WorkedPathRequest='Supplemental materials/Game tree diagrams/worked equilibrium paths.request.json';
    MultipleEquilibriaDirectory='Supplemental materials/Multiple equilibria'
}
$config | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $article 'article-diagrams.json') -Encoding utf8
Write-Output 'Imported the verified collection. Supplemental workflows retained and rebased; manuscript folders ready for numbered assembly.'
