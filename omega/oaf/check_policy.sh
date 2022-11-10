#!/bin/bash

# Example:
# python create-assertion.py --private-key private-key.pem -p pkg:npm/left-pad@1.3.0 --assertion ActivelyMaintained --repository https://github.com/madler/zlib > t1
# bash check_policy.sh pkg:npm/left-pad@1.3.0 assertions/reference-policies/actively_maintained.rego
# > PASS

PACKAGE_URL=$1
POLICY="$2"

# Check for errors
grep -qrE "package.+\.${POLICY}" assertions/policies
if [ $? -ne 0 ]; then
    echo "ERROR: Policy not found"
    exit 1
fi

# Fetch assertions from the database
TEMP_DIR="/tmp/omega/chk-$(uuidgen -r)"
if [ -d "$TEMP_DIR" ]; then
    echo "ERROR: $TEMP_DIR already exists, this should never occur."
    exit 1
fi
mkdir -p $TEMP_DIR
echo "Fetching assertions to $TEMP_DIR"
python fetch_assertions.py --package-url "$PACKAGE_URL" --sqlite-db ../analyzer/worker/assertions.db --directory "$TEMP_DIR"

#RESULT=$(opa eval -i "${DATA}" -b assertions/policies "data.openssf.omega.policy.${POLICY}" --format json)
#ERRORS=$(echo "${RESULT}" | jq '.errors')
#if [[ "${ERRORS}" != "null" ]]; then
#    echo "ERROR: An error occurred while processing the policies. Unable to continue."
#    echo "${ERRORS}"
#    exit 1
#fi

for FILENAME in ${TEMP_DIR}/*; do
    #echo "Processing $FILENAME"

    #echo "Verifying assertions..."
    python check-assertion-trust.py --assertion "${FILENAME}" --trusted-keys ./public-key.pem
    if [ $? -ne 0 ]; then
        #echo "ERROR: Assertion failed to verify, removing from list."
        rm "${FILENAME}"
        continue
    fi

    APPLIES=$(opa eval -i "${FILENAME}" -b assertions/policies "data.openssf.omega.policy.${POLICY}.applies" --format pretty)

    if [ "${APPLIES}" = "true" ]; then
        PASS=$(opa eval -i "${FILENAME}" -b assertions/policies "data.openssf.omega.policy.${POLICY}.pass" --format pretty)
        if [ "${PASS}" = "true" ]; then
            echo "[${POLICY}] PASS"
        else
            echo "[${POLICY}] FAIL"
        fi
    #else
        #echo "[${POLICY}] NOT APPLICABLE"
    fi
done

rm -rf "$TEMP_DIR"