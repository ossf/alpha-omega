param(
    [Parameter(Mandatory=$false)]
    [bool]
    $force = $false
)

try
{
    $version = (Select-String -Path Dockerfile -Pattern 'LABEL Version="(.*)"').Matches.Groups[1].Value
    
    if ($force) {
        docker build -t openssf/omega-toolshed:$version . -f Dockerfile --build-arg CACHEBUST=$(date -Format o)
    } else {
        docker build -t openssf/omega-toolshed:$version . -f Dockerfile
    }
    docker tag openssf/omega-toolshed:$version openssf/omega-toolshed:latest
}
catch
{
    Write-Host "Error running build."
}
