#!/bin/bash

# Example:
# python create-assertion.py --private-key private-key.pem -p pkg:npm/left-pad@1.3.0 --assertion ActivelyMaintained --repository https://github.com/madler/zlib > t1
# bash check_policy.sh ./t1 assertions/reference-policies/actively_maintained.rego
# true

DATA="$1"
POLICY="$2"

# Check for errors
RESULT=$(opa eval -i "${DATA}" -b assertions/policies "data.openssf.omega.policy.${POLICY}" --format json)
ERRORS=$(echo "${RESULT}" | jq '.errors')
if [[ "${ERRORS}" != "null" ]]; then
    echo "An error occurred while processing the policies. Unable to continue."
    echo "${ERRORS}"
    exit 1
fi

APPLIES=$(opa eval -i "${DATA}" -b assertions/policies "data.openssf.omega.policy.${POLICY}.applies" --format pretty)

if [ "${APPLIES}" = "true" ]; then
    PASS=$(opa eval -i "${DATA}" -b assertions/policies "data.openssf.omega.policy.${POLICY}.pass" --format pretty)
    if [ "${PASS}" = "true" ]; then
        echo "[${POLICY}] PASS"
    else
        echo "[${POLICY}] FAIL"
    fi
else
    echo "[${POLICY}] NOT APPLICABLE"
fi