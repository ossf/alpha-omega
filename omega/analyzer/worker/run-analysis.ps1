param (
    [Parameter(Mandatory=$true)]
    [string]
    $PackageUrl,

    [Parameter(Mandatory=$false)]
    [string]
    $PreviousVersion,
    
    [Parameter(Mandatory=$false)]
    [string]
    $OutputDirectoryName = "output",

    [Parameter(Mandatory=$false)]
    [string]
    $LibrariesIOAPIKey
)

$IMAGE_TAG = "0.6.7"

# Does directory exist?
if (Test-Path $OutputDirectoryName)
{
    Write-Host "Output directory already exists.  Please remove it before running this script."
    exit 1
}

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
Write-Output "Creating security review..."
cd tools
New-Item -ItemType Directory -Force -Path security-reviews | Out-Null
python create-review.py -i $OutputDirectoryName -p $PackageUrl -r security-reviews
cd ..
Write-Output "Security review created."
