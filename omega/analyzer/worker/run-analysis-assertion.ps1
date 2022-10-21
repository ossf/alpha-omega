param (
    [Parameter(Mandatory=$true)]
    [string]
    $PackageUrl,

    [Parameter(Mandatory=$false)]
    [string]
    $PreviousVersion,

    [Parameter(Mandatory=$false)]
    [string]
    $OutputDirectoryName = "results",

    [Parameter(Mandatory=$false)]
    [string]
    $LibrariesIOAPIKey
)

$IMAGE_TAG = "latest"

# Create directory, get absolute path for Docker
New-Item -ItemType Directory -Force -Path $OutputDirectoryName | Out-Null
$OutputDirectoryName = (Resolve-Path $OutputDirectoryName).Path

# Ensure we have a version
if (!$PackageUrl.Contains("@")) {
    $parts = $PackageUrl -split "/"
    $Name = $parts[1]
    $Type = ($parts[0] -split ":")[1]
    $res = Invoke-WebRequest -UseBasicParsing -Uri "http://deps.dev/_/s/$Type/p/$Name"
    $data = $res.Content | ConvertFrom-Json
    $version = $data.version.version
    $PackageUrl = "pkg:$Type/$Name@$version"
    Write-Host "Normalized PackageUrl to $PackageUrl"
}


if ($LibrariesIOAPIKey -ne $null)
{
    docker run --rm -it -e "LIBRARIES_IO_API_KEY=$LibrariesIOAPIKey" --mount type=bind,source=$OutputDirectoryName,target=/opt/export openssf/omega-toolshed:$IMAGE_TAG $PackageUrl $PreviousVersion
}
else
{
    docker run --rm -it --mount type=bind,source=$OutputDirectoryName,target=/opt/export openssf/omega-toolshed:$IMAGE_TAG $PackageUrl $PreviousVersion
}
Write-Output "Package successfully analyzed, results in $OutputDirectoryName"

# Create security review (if needed)
Write-Output "Running assertions..."

cd tools
Get-ChildItem -Path $OutputDirectoryName -Filter '*.sarif' -Recurse | %{
    python .\create-assertion.py --assertion NoCriticalSecurityFindingsByTool --package-url $PackageUrl --private-key private-key.pem --input_file $_.FullName > $OutputDirectoryName\assertion-no-critical-security-findings-by-tool__{$_.Name}.json
}
python .\create-assertion.py --assertion NoPubliclyKnownVulnerabilities --package-url $PackageUrl --private-key private-key.pem > $OutputDirectoryName\assertion-no-publicly-known-vulnerabilities.json
cd ..

Write-Output "Operation Complete"
