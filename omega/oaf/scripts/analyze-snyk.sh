#!/bin/bash
### !!! TODO: This has not been migrated to v2 yet.

PACKAGE="$1"
if [ -z "$PACKAGE" ]; then
    echo "Usage: analyze-snyk.sh package_url"
    exit 1
fi

TEMP_DIR="/tmp/omega/chk-$(uuidgen -r)"
if [ -d "$TEMP_DIR" ]; then
    echo "ERROR: $TEMP_DIR already exists, this should never occur."
    exit 1
fi
mkdir -p "$TEMP_DIR"

CUR_PATH=$(pwd)
cd "${TEMP_DIR}"
echo "Downloading $PACKAGE..."

# if package contains an @ symbol, it's a specific version
if [[ "$PACKAGE" == *"@"* ]]; then
    PACKAGE_NAME=$(echo "$PACKAGE" | cut -d "@" -f 1)
    VERSION=$(echo "$PACKAGE" | cut -d "@" -f 2)
    oss-download -e "${PACKAGE}" 2>&1 >/dev/null
else
    PACKAGE_NAME="$PACKAGE"
    VERSION=$(oss-download -e "${PACKAGE}" 2>&1 | grep -Eo 'INFO.*Downloaded.*' | cut -d@ -f2)
fi

cd "${CUR_PATH}"

if [ "$(ls -A ${TEMP_DIR})" ]; then
    echo "Target: $PACKAGE_NAME@$VERSION"
    RESULT=$(snyk code test --severity-threshold=medium "${TEMP_DIR}")

    NUM_CRITICAL=$(echo "$RESULT" | grep -iEo '[0-9]+ \[Critical\]' | cut -d" " -f1)
    [[ $NUM_CRITICAL =~ ^[0-9]+$ ]] || NUM_CRITICAL=0
    NUM_HIGH=$(echo "$RESULT" | grep -iEo '[0-9]+ \[High\]' | cut -d" " -f1)
    [[ $NUM_HIGH =~ ^[0-9]+$ ]] || NUM_HIGH=0
    NUM_MEDIUM=$(echo "$RESULT" | grep -iEo '[0-9]+ \[Medium\]' | cut -d" " -f1)
    [[ $NUM_MEDIUM =~ ^[0-9]+$ ]] || NUM_MEDIUM=0

    cd ..
    python create-assertion.py --package-url "${PACKAGE}" --private-key ../private-key.pem --assertion ManualAssertion --metadata '{"name": "openssf.omega.snyk", "version": "0.1.0"}' --predicate "{\"content\": {\"critical\": $NUM_CRITICAL, \"high\": $NUM_HIGH, \"medium\": $NUM_MEDIUM}}"
else
    echo "No package found for $PACKAGE_NAME@$VERSION"
fi

rm -rf "${TEMP_DIR}"
cd "${CUR_PATH}"