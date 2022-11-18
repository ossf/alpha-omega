#!/bin/bash

set -e

# Download the OpenPolicyAgent binary
if [ -f "opa" ]; then
    echo "INFO:  OpenPolicyAgent already exists, remove and re-run to download again."
else
    OPA_VERSION="v0.46.1"
    curl -s -L -o opa_linux_amd64_static "https://openpolicyagent.org/downloads/${OPA_VERSION}/opa_linux_amd64_static"
    curl -s -L -o opa_linux_amd64_static.sha256 "https://openpolicyagent.org/downloads/${OPA_VERSION}/opa_linux_amd64_static.sha256"
    shasum -c opa_linux_amd64_static.sha256
    echo "INFO:  OpenPolicyAgent downloaded successfully, checksum matches."
    rm opa_linux_amd64_static.sha256
    mv opa_linux_amd64_static opa
    chmod +x opa
fi

# Check Python
python -V > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Python is not installed. Please install and re-run this script."
    exit 1
fi

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "INFO:  Creating virtual environment..."
    python -mvenv venv
    venv/bin/pip install -r requirements.txt
fi

if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "INFO:  Please run 'source venv/bin/activate' to activate the virtual environment, then re-run this script."
    exit 1
fi

echo "INFO:  Initialization complete. Run 'check_policy.sh' to get started."