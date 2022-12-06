#!pwsh

param (
    [Parameter(Mandatory=$true)]
    [string]
    $PackageUrl,

    [Parameter(Mandatory=$false)]
    [string]
    $PreviousVersion,

    [Parameter(Mandatory=$false)]
    [string]
    $OutputDirectoryName = "results"
)

$IMAGE_TAG = "latest"

# Check for Python virtual environment
if (!(Get-Command "python" -errorAction SilentlyContinue)) {
    Write-Error "Python was not found, unable to continue. Please install and re-run."
    Exit 1
}
if (!(Get-Command "dotnet" -ErrorAction SilentlyContinue)) {
    Write-Error ".NET was not found, unable to continue. Please install and re-run."
    Exit 1
}
if (!(Get-Command "RecursiveExtractor" -ErrorAction SilentlyContinue)) {
    Write-Error "RecursiveExtractor was not found, unable to continue. Please install and re-run."
    Write-Error "dotnet tool install microsoft.cst.recursiveextractor.cli"
    Exit 1
}

Set-Location "tools"
if (!(Test-Path "venv" -PathType Container)) {
    Write-Warning "Virtual environment not found, creating..."
    python -mvenv venv
    sh -c "source ./venv/bin/activate && pip install -r requirements.txt"
}
Set-Location ".."

# Check for an environment variable file
if (!(Test-Path ".env")) {
    Write-Warning "Missing .env, some features will not be available. See .env.example for information."
}

# Create directory, get absolute path for Docker
New-Item -ItemType Directory -Force -Path $OutputDirectoryName | Out-Null
$OutputDirectoryName = (Resolve-Path $OutputDirectoryName).Path

# If we're not provided a version, get the latest version from deps.dev.
# BUG: Do we handle namespaces nicely here?
if (!$PackageUrl.Contains("@")) {
    $parts = $PackageUrl -split "/"
    $PackageName = $parts[1]
    $PackageType = ($parts[0] -split ":")[1]
    $res = Invoke-WebRequest -UseBasicParsing -Uri "http://deps.dev/_/s/$PackageType/p/$PackageName"
    $data = $res.Content | ConvertFrom-Json
    $PackageVersion = $data.version.version
    $PackageUrl = "pkg:$PackageType/$PackageName@$PackageVersion"
    Write-Host "Normalized PackageUrl to $PackageUrl"
}

if (Test-Path ".env")
{
    docker run --rm -t --env-file .env -v "$OutputDirectoryName`:/opt/export" openssf/omega-toolshed:$IMAGE_TAG $PackageUrl $PreviousVersion
}
else
{
    docker run --rm -t -v "$OutputDirectoryName`:/opt/export" openssf/omega-toolshed:$IMAGE_TAG $PackageUrl $PreviousVersion
}
Write-Output "Package successfully analyzed, results in $OutputDirectoryName"

Write-Output "Normalizing file references..."
Set-Location "tools"
$parts = $PackageUrl -split "/"
$PackageName = ($parts[1] -split "@")[0].ToLower()
$PackageType = ($parts[0] -split ":")[1].ToLower()
$PackageVersion = ($PackageUrl -split "@")[1].ToLower()
Write-Output "$OutputDirectoryName/$PackageType/$PackageName/$PackageVersion"
./venv/bin/python normalize-sarif-to-source.py --sarif-dir "$OutputDirectoryName/$PackageType/$PackageName/$PackageVersion"
Set-Location ..

# Creating assertions
Write-Output "Running assertions..."

Set-Location "tools"
Get-ChildItem -Path "$OutputDirectoryName/$PackageType/$PackageName/$PackageVersion" -Filter '*.sarif' -Recurse | ForEach-Object {
    ./venv/bin/python ./create-assertion.py --assertion NoCriticalSecurityFindingsByTool --package-url $PackageUrl --private-key private-key.pem --input_file $_.FullName > "$OutputDirectoryName/$PackageType/$PackageName/$PackageVersion/assertion-no-critical-security-findings-by-tool__$($_.BaseName).json"
}
./venv/bin/python ./create-assertion.py --assertion NoPubliclyKnownVulnerabilities --package-url $PackageUrl --private-key private-key.pem > "$OutputDirectoryName/$PackageType/$PackageName/$PackageVersion/assertion-no-publicly-known-vulnerabilities.json"
Set-Location ..

Write-Output "Operation Complete"
