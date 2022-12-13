#
# This script starts the Omega Analysis Toolchain and drops you into a shell with /opt/export mapped to ./results.
#

# Create directory "results" only if it doesn't already exist
if (-Not (Test-Path "results" -PathType Container))
{
    New-Item -ItemType Directory -Force -Path "results" | Out-Null
}

Write-Host "Running the Omega Analysis Toolchain..."
if (Test-Path ".env")
{
    docker run --rm -it --env-file .env --mount "type=bind,source=$(Get-Location)/results,target=/opt/export" --entrypoint /bin/bash openssf/omega-toolshed:latest
}
else
{
    Write-Host "Running without an environment file (.env). Some features will not be available within the container. See .env.example for an example."
    docker run --rm -it --mount "type=bind,source=$(Get-Location)/results,target=/opt/export" --entrypoint /bin/bash openssf/omega-toolshed:latest
}
