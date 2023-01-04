#!/bin/bash

CLONE_URL=$(cat results.sarif | jq '.runs[0].versionControlProvenance[0].repositoryUri' | cut -d\" -f2)
COMMIT_HASH=$(cat results.sarif | jq '.runs[0].versionControlProvenance[0].revisionId' | cut -d\" -f2)
echo $CLONE_URL
echo $COMMIT_HASH

git clone "$CLONE_URL" work
cd work
git checkout "$COMMIT_HASH"
rm -rf .git
cp ../results.sarif .
cd ..
