#!/bin/bash

# Pull down Azurite if needed
IMAGE_ID=$(docker image ls mcr.microsoft.com/azure-storage/azurite -q)
if [ -z "$IMAGE_ID" ]; then
       docker pull mcr.microsoft.com/azure-storage/azurite
fi

# Start Azurite
echo "(Re-)Starting Azurite..."
docker start azurite || docker run --name azurite -d --restart unless-stopped \
       -p 10000:10000 \
       -v $(pwd)/azurite-data:/data \
       mcr.microsoft.com/azure-storage/azurite

# Configure the virtual environment
if [ ! -d "venv" ]; then
       echo "Creating virtual environment..."
       python3 -m venv venv
       source venv/bin/activate
       pip install -r service-endpoint/requirements.txt
else
       source venv/bin/activate
fi

if [ ! -d "azure_function_core_sdk" ]; then
       echo "Installing Azure Function Core SDK..."
       VERSION=$(curl https://api.github.com/repos/Azure/azure-functions-core-tools/releases | jq '.[0].name' | cut -d\" -f2)
       wget "https://github.com/Azure/azure-functions-core-tools/releases/download/$VERSION/Azure.Functions.Cli.linux-x64.$VERSION.zip"
       unzip -d azure_function_core_sdk "Azure.Functions.Cli.linux-x64.$VERSION.zip"
       rm "Azure.Functions.Cli.linux-x64.$VERSION.zip"
       chmod +x azure_function_core_sdk/func
fi

# Ensure it's on the path
func --help >/dev/null 2>&1
if [ $? -ne 0 ]; then
       echo "Adding Azure Function Core SDK to PATH..."
       export PATH="$(pwd)/azure_function_core_sdk:$PATH"
fi

cd service-endpoint
func start
cd ..
