# Create directory "output" only if it doesn't already exist
if (-Not (Test-Path "output" -PathType Container))
{
    New-Item -ItemType Directory -Force -Path "results" | Out-Null
}

Write-Host "Running the Omega Analysis Toolchain..."
if (Test-Path ".env")
{
    docker run --rm -it --env-file .env --mount type=bind,source=$(pwd)\results,target=/opt/export --entrypoint /bin/bash openssf/omega-toolshed:latest
}
else
{
    Write-Host "Running without an environment file (.env). Some features will not be available within the container. See .env.example for an example."
    docker run --rm -it --mount type=bind,source=$(pwd)\results,target=/opt/export --entrypoint /bin/bash openssf/omega-toolshed:latest
}
