#!pwsh

param (
    [Parameter(Mandatory=$true)]
    [string]
    $Directory,

    [Parameter(Mandatory=$false)]
    [string]
    $PackageName = "",

    [Parameter(Mandatory=$false)]
    [string]
    $OutputDirectoryName = "results"
)

$IMAGE_TAG = "latest"

#
# This script starts the Omega Analysis Toolchain against a local source folder, instead of a package.
#

if (-Not (Test-Path $Directory -PathType Container))
{
    Write-Error "Directory [$Directory] does not exist - what do you want to analyze?"
    exit 1
}

# Create directory only if it doesn't already exist
if (-Not (Test-Path $OutputDirectoryName -PathType Container))
{
    New-Item -ItemType Directory -Force -Path $OutputDirectoryName | Out-Null
}
if ($PackageName -eq "")
{
    $PackageName = (Split-Path (Resolve-Path $Directory) -Leaf)
}

# This is how you pass a PackageURL to Toolshed but have it treat it like a folder.
# The "local_source=true" is the important part.
# Toolshed looks in /opt/local_source for the source code, so you need to map it there.
$PackageName = $PackageName -replace "\s", ""
$PackageUrl = "pkg:generic/$PackageName@1.0.0?local_source=true"

Write-Host "Running the Omega Analysis Toolchain..."
if (Test-Path ".env")
{
    docker run --rm -it --env-file .env --mount "type=bind,source=$(Resolve-Path $Directory),target=/opt/local_source" --mount "type=bind,source=$(Get-Location)/results,target=/opt/export" openssf/omega-toolshed:$IMAGE_TAG $PackageUrl
}
else
{
    Write-Host "Running without an environment file (.env). Some features will not be available within the container. See .env.example for an example."
    docker run --rm -it --mount "type=bind,source=$(Resolve-Path $Directory),target=/opt/local_source" --mount "type=bind,source=$(Get-Location)/results,target=/opt/export" openssf/omega-toolshed:$IMAGE_TAG $PackageUrl
}
