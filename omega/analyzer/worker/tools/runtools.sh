#!/bin/bash

###############################################################################
# Open Source Security Foundation (OpenSSF)
# Alpha-Omega
# Analyzer: runtools.sh
#
# This script can be used to analyze a given package using a set of analyzers.
#
# Usage: runtool.sh PACKAGE_URL
#
# Output:
#  Output is writted to /opt/export
#
# Copyright (c) Microsoft Corporation. Licensed under the Apache License.
###############################################################################
tabs 4

# Specify the package to analyze either through a parameter or environment variable
if [ "$#" -lt 1 ]; then
    echo "Usage: runtools.sh PACKAGE_URL [PREVIOUS VERSION]"
    exit 1
fi
PURL="$1"

# Used to keep duration of individual jobs
function event()
{
    echo "$1,$2,$SECONDS" >> /tmp/events.txt
}

# Attempts to identify the previous version of a component dynamically
function get_previous_version()
{
    if [ -z "$LIBRARIES_IO_API_KEY" ]; then
        if [ -n "$PACKAGE_OVERRIDE_PREVIOUS_VERSION" ]; then
            echo "$PACKAGE_OVERRIDE_PREVIOUS_VERSION"
        else
            printf "${BG_RED}${WHITE}Missing LIBRARIES_IO_API_KEY. Unable to identify previous version.${NC}\n" 1>&2
        fi
        return
    fi
    METADATA=$(curl -L -s "https://libraries.io/api/$PACKAGE_PURL_TYPE/$PACKAGE_PURL_NAMESPACE_NAME_ENCODED?api_key=$LIBRARIES_IO_API_KEY" | jq .)
    if [ -n "$METADATA" ]; then
        CUR_VERSION_EXISTS=$(echo "$METADATA" | jq '[.versions[] | {"version": .number, "published_at": .published_at}]' | grep -F -B4 "\"$PACKAGE_PURL_VERSION\"")
        # Libraries.io doesn't always have the latest package -- if so, then just take the maximum as the "previous".
        if [ -z "$CUR_VERSION_EXISTS" ]; then
            PREV_VERSION_BY_DATE=$(echo "$METADATA" | jq '[.versions[] | {"version": .number, "published_at": .published_at}]' | jq 'sort_by(.published_at)' | grep \"version\" | tail -1 | cut -d\" -f4)
            PREV_VERSION_BY_NUMBER="$PREV_VERSION_BY_DATE"
        else
            PREV_VERSION_BY_DATE=$(echo "$METADATA" | jq '[.versions[] | {"version": .number, "published_at": .published_at}]' | jq 'sort_by(.published_at)' | grep -F -B4 "\"$PACKAGE_PURL_VERSION\"" | head -1 | cut -d\" -f4)
            PREV_VERSION_BY_NUMBER=$(echo "$METADATA" | jq '.versions[] | .number' | sed 's/\"//g' | sort -V | grep -Fx -B1 "$PACKAGE_PURL_VERSION" | head -1)
        fi
        if [ "$PREV_VERSION_BY_DATE" != "[" ]; then
            echo "$PREV_VERSION_BY_DATE"
        fi
        if [ "$PREV_VERSION_BY_DATE" != "$PREV_VERSION_BY_NUMBER" ] && [ "$PREV_VERSION_BY_NUMBER" != "[" ] && [ "$PREV_VERSION_BY_NUMBER" != "$PACKAGE_PURL_VERSION" ]; then
            echo "$PREV_VERSION_BY_NUMBER"
        fi
    fi
}

# Start the Script!

event start runtools

START_TIME=$(date +%s)

# If NO_COLOR env var is set, do not display any color https://no-color.org/
if [ -z "${NO_COLOR}" ]; then
    WHITE='\033[37;1m'
    DARKGRAY='\033[30;1m'
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    BG_RED='\033[41m'
    NC='\033[0m'
else
    WHITE=''
    DARKGRAY=''
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    BG_RED=''
    NC=''
fi

LONG_ANALYZER_TIMEOUT="60m"

BUILD_SCRIPT_ROOT="/opt/buildscripts"

PACKAGE_PURL_PARSED=$(python /opt/toolshed/parse_purl.py "${PURL}")
PACKAGE_PURL_TYPE=$(echo "${PACKAGE_PURL_PARSED}" | grep "PACKAGE_TYPE:" | cut -d: -f2-)
PACKAGE_PURL_NAME=$(echo "${PACKAGE_PURL_PARSED}" | grep "PACKAGE_NAME:" | cut -d: -f2-)
PACKAGE_PURL_NAME_ENCODED=$(echo "${PACKAGE_PURL_PARSED}" | grep "PACKAGE_NAME_ENCODED:" | cut -d: -f2-)
PACKAGE_PURL_NAMESPACE_NAME=$(echo "${PACKAGE_PURL_PARSED}" | grep "PACKAGE_NAMESPACE_NAME:" | cut -d: -f2-)
PACKAGE_PURL_NAMESPACE_NAME_ENCODED=$(echo "${PACKAGE_PURL_PARSED}" | grep "PACKAGE_NAMESPACE_NAME_ENCODED:" | cut -d: -f2-)
PACKAGE_PURL_VERSION=$(echo "${PACKAGE_PURL_PARSED}" | grep "PACKAGE_VERSION:" | cut -d: -f2-)
PACKAGE_PURL_OVERRIDE_URL=$(echo "${PACKAGE_PURL_PARSED}" | grep "PACKAGE_QUALIFIERS_URL:" | cut -d: -f2-)
PACKAGE_PURL=$(echo "${PACKAGE_PURL_PARSED}" | grep "PACKAGE_PURL:" | cut -d: -f2-)
PACKAGE_DIR=$(echo "${PACKAGE_PURL_PARSED}" | grep "PACKAGE_DIR:" | cut -d: -f2-)
PACKAGE_DIR_NOVERSION=$(echo "${PACKAGE_PURL_PARSED}" | grep "PACKAGE_DIR_NOVERSION:" | cut -d: -f2-)

# if destination dir specified in env, take that instead of /opt/export
if ([ -n "${DESTINATION_DIR}" ] && [ -d "${DESTINATION_DIR}" ]); then
    EXPORT_DIR="${DESTINATION_DIR}/${PACKAGE_DIR}"
else
    # check for parameter substitution
    if ([ -n "${DESTINATION_DIR}" ] && [ -d "${!DESTINATION_DIR}" ]); then
        EXPORT_DIR="${!DESTINATION_DIR}/${PACKAGE_DIR}"
    else
        EXPORT_DIR="/opt/export/${PACKAGE_DIR}"
    fi
fi
mkdir -p "$EXPORT_DIR"

# Fix the OSSGadget Package URL when we have scoped namespaces
PACKAGE_PURL_OSSGADGET="${PURL}"
if [[ "$PACKAGE_PURL_NAMESPACE_NAME" == @* ]]; then
    PACKAGE_PURL_OSSGADGET="pkg:${PACKAGE_PURL_TYPE}/${PACKAGE_PURL_NAMESPACE_NAME_ENCODED}@${PACKAGE_PURL_VERSION}"
fi

PACKAGE_OVERRIDE_PREVIOUS_VERSION="$2"

ANALYZER_VERSION="0.8.0"
ANALYSIS_DATE=$(date)

# ASCII Art generated using http://patorjk.com/software/taag/#p=display&h=0&v=0&c=echo&f=THIS&t=Toolshed
printf "\n"
printf "${BLUE}The Open Source Security Foundation - Alpha-Omega${NC}\n";
printf "${YELLOW} ▄▀▀▀█▀▀▄  ▄▀▀▀▀▄   ▄▀▀▀▀▄   ▄▀▀▀▀▄      ▄▀▀▀▀▄  ▄▀▀▄ ▄▄   ▄▀▀█▄▄▄▄  ▄▀▀█▄▄  \n";
printf "${YELLOW}█    █  ▐ █      █ █      █ █    █      █ █   ▐ █  █   ▄▀ ▐  ▄▀   ▐ █ ▄▀   █ \n";
printf "${YELLOW}▐   █     █      █ █      █ ▐    █         ▀▄   ▐  █▄▄▄█    █▄▄▄▄▄  ▐ █    █ \n";
printf "${YELLOW}   █      ▀▄    ▄▀ ▀▄    ▄▀     █       ▀▄   █     █   █    █    ▌    █    █ \n";
printf "${YELLOW} ▄▀         ▀▀▀▀     ▀▀▀▀     ▄▀▄▄▄▄▄▄▀  █▀▀▀     ▄▀  ▄▀   ▄▀▄▄▄▄    ▄▀▄▄▄▄▀ \n";
printf "${YELLOW}█ ${BLUE}omega-help${YELLOW}@${BLUE}openssf.org${YELLOW}      █          ▐       █   █     █    ▐   █     ▐  \n";
printf "${YELLOW}▐                             ▐                  ▐   ▐     ▐        ▐ ${DARKGRAY}v${ANALYZER_VERSION}${NC}\n\n";

printf "${BLUE}Starting at: ${YELLOW}${ANALYSIS_DATE}${NC}\n"

if [ -z "$PACKAGE_PURL_TYPE" ] || [ -z "$PACKAGE_PURL_NAME" ] || [ -z "$PACKAGE_PURL_VERSION" ]; then
    printf "${BG_RED}${WHITE}Unable to parse Package URL: [${PURL}]${NC}\n"
    exit 1
fi

printf "${BLUE}Analyzing: ${YELLOW}${PACKAGE_PURL_TYPE} ${DARKGRAY}/ ${YELLOW}"
printf "%s" "${PACKAGE_PURL_NAMESPACE_NAME}"
printf " ${DARKGRAY}/ ${YELLOW}"
printf "%s" "${PACKAGE_PURL_VERSION}"
printf "${BLUE}...${NC}\n"

TOP_ROOT="/opt/src/${PACKAGE_DIR_NOVERSION}"
CUR_ROOT="/opt/src/${PACKAGE_DIR}"
mkdir -p /opt/result "$TOP_ROOT" "$CUR_ROOT" "$CUR_ROOT/reference-binaries" "$CUR_ROOT/src" "$CUR_ROOT/installed"

PREVIOUS_VERSIONS=""
if [ -z "$PACKAGE_PURL_OVERRIDE_URL" ]; then
    PREVIOUS_VERSIONS=$(get_previous_version)
    if [ -n "$PREVIOUS_VERSIONS" ]; then
        printf "${GREEN}Found previous versions: ${PREVIOUS_VERSIONS//$'\n'/}${NC}\n"
    fi
fi

# OSS Gadget - Download binaries, store away for safekeeping
printf "${RED}Downloading binaries...${NC}\n"
event start download-binaries
cd "$CUR_ROOT/reference-binaries"
if [ -z "$PACKAGE_PURL_OVERRIDE_URL" ]; then
    oss-download "$PACKAGE_PURL_OSSGADGET" >>/opt/result/admin-download.log 2>&1
else
    oss-download "pkg:url/$PACKAGE_PURL_NAME_ENCODED@$PACKAGE_PURL_VERSION?url=$PACKAGE_PURL_OVERRIDE_URL" >>/opt/result/admin-download.log 2>&1
fi
event stop download-binaries
if [ -z "$(ls -A "$CUR_ROOT"/reference-binaries 2>/dev/null)" ]; then
    printf "${BG_RED}${WHITE}Package could not be found, nothing to do.${NC}\n"
    exit 1
fi
cd "$CUR_ROOT"
cp -R reference-binaries /opt/result

# Download and extract the package
printf "${RED}Extracting binaries...${NC}\n"
cd "$CUR_ROOT/src"
event start download-and-extract-binaries
if [ -z "$PACKAGE_PURL_OVERRIDE_URL" ]; then
    oss-download -e "$PACKAGE_PURL_OSSGADGET" >>/opt/result/admin-download.log 2>&1
else
    oss-download -e "pkg:url/$PACKAGE_PURL_NAME_ENCODED@$PACKAGE_PURL_VERSION?url=$PACKAGE_PURL_OVERRIDE_URL" >>/opt/result/admin-download.log 2>&1
fi
# Previous versions (only if override url isn't set)
for PREVIOUS_VERSION in $PREVIOUS_VERSIONS; do
    printf "${RED}Extracting previous version: ${PREVIOUS_VERSION}${NC}\n"
    mkdir -p "$TOP_ROOT/$PREVIOUS_VERSION/src"
    cd "$TOP_ROOT/$PREVIOUS_VERSION/src"
    VERSION_ENCODED="pkg:${PACKAGE_PURL_TYPE}/${PACKAGE_PURL_NAMESPACE_NAME_ENCODED}@${PREVIOUS_VERSION}"
    oss-download -e "$VERSION_ENCODED" >>/opt/result/admin-download.log 2>&1
done
cd "$CUR_ROOT"
event stop download-and-extract-binaries

printf "${RED}Decompiling .NET binaries...${NC}\n"
event start decompile-dotnet-binaries
find "$CUR_ROOT/src" -type f -print0 | xargs -0 file | grep -Fi ".net assembly" | cut -d: -f1 | xargs -I{} -n1 bash -c "F='{}'; echo \"Processing \$F\"; mkdir -p \"$CUR_ROOT/decompiled/\$F\"; /root/.dotnet/tools/ilspycmd \"\$F\" -genpdb -p -o \"$CUR_ROOT/decompiled/\$F\"" >>/opt/result/admin-decompilation.log 2>&1
for PREVIOUS_VERSION in $PREVIOUS_VERSIONS; do
    printf "${RED}Decompiling previous version: ${PREVIOUS_VERSION}${NC}\n"
    mkdir -p "$TOP_ROOT/$PREVIOUS_VERSION/decompiled"
    find "$TOP_ROOT/$PREVIOUS_VERSION/src" -type f -print0 | xargs -0 file | grep -Fi ".net assembly" | cut -d: -f1 | xargs -I{} -n1 bash -c "F='{}'; echo \"Processing \$F\"; mkdir -p \"$TOP_ROOT/$PREVIOUS_VERSION/decompiled/\$F\"; /root/.dotnet/tools/ilspycmd \"\$F\" -genpdb -p -o \"$TOP_ROOT/$PREVIOUS_VERSION/decompiled/\$F\"" >>/opt/result/admin-decompilation.log 2>&1
done
event stop decompile-dotnet-binaries

# Calculate all checksums
printf "${RED}Calculating checksums...${NC}\n"
event start calculate-checksums
find "$TOP_ROOT" -type f -exec sha256sum {} \; >/opt/result/admin-file-checksums.txt
event stop calculate-checksums

# Distinct File Types
printf "${RED}Calculating file types..${NC}\n"
event start calculate-file-types
FILE_TYPES=". $(scc "/opt/src" --ci | cut -d" " -f1 | grep -Evi "language|total|estimated|processed|------" | tr '[:upper:]' '[:lower:]' | paste -sd " " -) ."
FILE_TYPES="$FILE_TYPES . $(find "/opt/src" -type f | awk -F. '!a[$NF]++{print $NF}' | tr '[:upper:]' '[:lower:]' | paste -sd " " -) ."
event stop calculate-file-types

# Calculating Code Size
printf "${RED}Calculating code size..${NC}\n"
event start calculate-code-size
scc --ci -z "$CUR_ROOT/src" >/opt/result/tool-scc.txt 2>/opt/result/tool-scc.error
event stop calculate-code-size

# Characteristics - via Application Inspector
printf "${RED}Identifying characteristics...${NC}\n"
event start tool-application-inspector
ApplicationInspector.CLI analyze -g none -s "$CUR_ROOT" -f json -o /opt/result/tool-application-inspector.json 2>/opt/result/tool-application-inspector.error >/dev/null
for PREVIOUS_VERSION in $PREVIOUS_VERSIONS; do
    # Characteristics Diff
    printf "${RED}Identifying new characteristics from version $PREVIOUS_VERSION...${NC}\n"
    ApplicationInspector.CLI tagdiff --src1 "$CUR_ROOT" --src2 "$TOP_ROOT/$PREVIOUS_VERSION" -g none -f json -o "/opt/result/tool-application-inspector-diff.$PREVIOUS_VERSION.json" >>/opt/result/tool-application-inspector.log 2>&1
done
event stop tool-application-inspector

# String Diff
printf "${RED}Identifying new strings from previous version...${NC}\n"
find "$CUR_ROOT" -type f | xargs -I{} grep -Eoa '\w+(\w\.)*\w+' {} | tr '[:upper:]' '[:lower:]' | sort | uniq >"/opt/result/tool-strings.$PACKAGE_PURL_VERSION.txt"
for PREVIOUS_VERSION in $PREVIOUS_VERSIONS; do
    find "$TOP_ROOT/$PREVIOUS_VERSION/" -type f | xargs -I{} grep -Eoa '\w+(\w\.)*\w+' {} | tr '[:upper:]' '[:lower:]' | sort | uniq > "/opt/result/tool-strings.$PREVIOUS_VERSION.txt"
    comm -23 "/opt/result/tool-strings.$PACKAGE_PURL_VERSION.txt" "/opt/result/tool-strings.$PREVIOUS_VERSION.txt" >"/opt/result/tool-strings-diff.$PACKAGE_PURL_VERSION-$PREVIOUS_VERSION.txt"
done

# Binary Attributes - via Radare2
printf "${RED}Extracting binary attributes via Radare2...${NC}\n"
find "$CUR_ROOT/src" -type f -print0 | xargs -0 file | grep -Eiv "text|json" | cut -d: -f1 | xargs -I{} -n1 bash -c "F='{}'; FN=\$(echo \$F | shasum -a256 | cut -d' ' -f1); echo \"{\"filename\": \"\$F\"}\" >/opt/result/tool-radare2-rabin2.\$FN.json; rabin2 -d -E -i -I -j -l -s -T -U -x -z -zz '{}' >>/opt/result/tool-radare2-rabin2.\$FN.json" >>/opt/result/tool-radare2-rabin2.log 2>&1

# Binary Attributes - via Binwalk
printf "${RED}Extracting binary attributes via Binwalk...${NC}\n"
mkdir -p /tmp/bw-entropy && cd /tmp/bw-entropy
find "$CUR_ROOT/src" -type f -print0 | xargs -0 file | grep -Eiv "text|json" | cut -d: -f1 | xargs -I{} -n1 bash -c "F='{}'; FN=$(echo \$F | shasum -a256 | cut -d' ' -f1); DR=\"$CUR_ROOT/binwalk_extracted/{}\"; mkdir -p "\$DR"; binwalk -B -A -e -M -C "\$DR" -E -J -f /opt/result/tool-binwalk.\$FN.txt {}; cp *.png /opt/result/tool-binwalk.entropy.\$FN.png" >>/opt/result/tool-binwalk.log 2>&1

# Bandit
if [[ $FILE_TYPES == *" python "* ]]; then
    printf "${RED}Running bandit...${NC}\n"
    cd "$CUR_ROOT/src"
    event start tool-bandit
    bandit -r -l -i --ignore-nosec -n 5 -f json "$CUR_ROOT/src" -o /opt/result/tool-bandit.json 2>/opt/result/tool-bandit.error
    event stop tool-bandit
fi

# Nodejsscan
if [[ "$FILE_TYPES" == *" javascript "* ]] || [[ "$FILE_TYPES" == *" typescript "* ]]; then
    printf "${RED}Running nodejsscan...${NC}\n"
    cd "$CUR_ROOT/src"
    event start tool-nodejsscan
    nodejsscan -d "$CUR_ROOT/src" -o /opt/result/tool-nodejsscan.json >/dev/null 2>/opt/result/tool-nodejsscan.error
    event stop tool-nodejsscan
fi

# Cryptography Detection
printf "${RED}Detecting cryptography...${NC}\n"
event start tool-oss-detect-cryptography
oss-detect-cryptography "$PACKAGE_PURL_OSSGADGET" >/opt/result/tool-oss-detect-cryptography.txt 2>/opt/result/tool-oss-detect-cryptography.error
event stop tool-oss-detect-cryptography

# Backdoor Detection
printf "${RED}Detecting backdoors...${NC}\n"
event start tool-oss-detect-backdoor
ApplicationInspector.CLI analyze -s "$CUR_ROOT" -i -r /opt/OSSGadget/Resources/BackdoorRules/ --scan-unknown-filetypes --no-show-progress -o /opt/result/tool-oss-detect-backdoor.json -f json --file-timeout 10000 >/opt/result/tool-oss-detect-backdoor.error 2>&1
event stop tool-oss-detect-backdoor

# Defogger
printf "${RED}Detecting obfuscated code...${NC}\n"
event start tool-oss-defog
oss-defog "$PACKAGE_PURL_OSSGADGET" >/dev/null 2>/opt/result/tool-oss-defog.txt
event stop tool-oss-defog

# Find Source
printf "${RED}Finding source repository...${NC}\n"
event start tool-oss-find-source
oss-find-source -f sarifv2 -o /opt/result/tool-oss-find-source.sarif "$PACKAGE_PURL_OSSGADGET" >/opt/result/tool-oss-find-source.stdout 2>/opt/result/tool-oss-find-source.stderr
event stop tool-oss-find-source

# DevSkim
printf "${RED}Running DevSkim...${NC}\n"
event start tool-devskim
devskim analyze --file-format sarif -d "$CUR_ROOT" >/opt/result/tool-devskim.sarif-noformat 2>/opt/result/tool-devskim.error
cat /opt/result/tool-devskim.sarif-noformat | jq > /opt/result/tool-devskim.sarif
rm /opt/result/tool-devskim.sarif-noformat
event stop tool-devskim

# CheckSec
printf "${RED}Checking binaries...${NC}\n"
event start tool-checksec
checksec --output=json --dir="$CUR_ROOT" >/opt/result/tool-checksec.json 2>/opt/result/tool-checksec.error
event stop tool-checksec

# ClamAV
printf "${RED}Detecting malware...${NC}\n"
event start tool-clamscan
clamscan --recursive=yes --detect-pua=yes --alert-encrypted=yes --alert-macros=yes --max-scantime=900 "$CUR_ROOT" >/opt/result/tool-clamscan.txt 2>/opt/result/tool-clamscan.error
event stop tool-clamscan

# Secrets Detection
printf "${RED}Detecting secrets - shhgit...${NC}\n"
event start tool-shhgit
shhgit -local "$CUR_ROOT" -csv-path /opt/result/tool-shhgit.csv >/dev/null 2>/opt/result/tool-shhgit.error
event stop tool-shhgit

printf "${RED}Detecting secrets - detect-secrets...${NC}\n"
event start tool-detect-secrets
detect-secrets scan --force-use-all-plugins --all-files "$CUR_ROOT" >/opt/result/tool-detect-secrets.json 2>/opt/result/tool-detect-secrets.log
event stop tool-detect-secrets

printf "${RED}Detecting secrets - secretscanner...${NC}\n"
event start tool-secretscanner
mkdir -p /tmp/secretscanner/work /tmp/secretscanner/output
cd /tmp/secretscanner
[ -f /tmp/secretscanner/config.yaml ] && rm /tmp/secretscanner/config.yaml
ln -s /root/go/pkg/mod/github.com/deepfence/*secret*scanner*/config.yaml
SecretScanner -config-path . -local "$CUR_ROOT" -debug-level DEBUG -temp-directory /tmp/secretscanner/work -multi-match -max-multi-match 20 -output-path /tmp/secretscanner/output >/opt/result/tool-secretscanner.log 2>&1
mv /tmp/secretscanner/output/*.json /opt/result/tool-secretscanner.json
chmod -x /opt/result/tool-secretscanner.json
event stop tool-secretscanner

# Binary to Source Validation
if [ "$PACKAGE_PURL_TYPE" == "npm" ]; then
    printf "${RED}Validating reproducibility - tbv...${NC}\n"
    event start tool-tbv
    timeout "$LONG_ANALYZER_TIMEOUT" tbv verify "$PACKAGE_PURL_NAMESPACE_NAME@$PACKAGE_PURL_VERSION" >/opt/result/tool-tbv.txt 2>/opt/result/tool-tbv.error
    sed -i 's/\x1b\[[0-9;]*m//g' /opt/result/tool-tbv.error
    event stop tool-tbv
fi

# Lizard (Code Complexity)
cd "$CUR_ROOT/src"
printf "${RED}Checking Code Complexity - lizard...${NC}\n"
event start tool-lizard
lizard -w "$CUR_ROOT/src" >/opt/result/tool-lizard.txt 2>/opt/result/tool-lizard.error
event stop tool-lizard

# Brakeman (Ruby)
if [ "$PACKAGE_PURL_TYPE" == "gem" ]; then
    cd "$CUR_ROOT/src"
    printf "${RED}Running Brakeman...${NC}\n"
    event start tool-brakeman
    brakeman -A --force-scan -f json "$CUR_ROOT/src" >/opt/result/tool-brakeman.json 2>/opt/result/tool-brakeman.log
    event stop tool-brakeman
fi

# CppCheck
if [[ "$FILE_TYPES" =~ ( )(c|h|hpp|c\+\+|cpp)( ) ]]; then
    cd "$CUR_ROOT/src"
    printf "${RED}Running CppCheck...${NC}\n"
    event start tool-cppcheck
    cppcheck --enable=all --quiet --template='{file}~!~{line}~!~{severity}~!~{message}~!~{code}~!~{id}~!~{cwe}' "$CUR_ROOT/src" >/opt/result/tool-cppcheck.json 2>/opt/result/tool-cppcheck.error
    event stop tool-cppcheck
fi

# Semgrep
cd "$CUR_ROOT/src"
printf "${RED}Running Semgrep...${NC}\n"
event start tool-semgrep
timeout "$LONG_ANALYZER_TIMEOUT" semgrep -f /opt/semgrep-rules --sarif >/opt/result/tool-semgrep.sarif-noformat 2>/opt/result/tool-semgrep.error
if [ $? -eq 124 ]; then
    echo "Semgrep timed out after $LONG_ANALYZER_TIMEOUT." >>/opt/result/tool-semgrep.error
else
    cat /opt/result/tool-semgrep.sarif-noformat | jq > /opt/result/tool-semgrep.sarif
    rm /opt/result/tool-semgrep.sarif-noformat
fi
event stop tool-semgrep

# Yara
printf "${RED}Running YARA...${NC}\n"
event start tool-yara
yara --print-strings -g -m /opt/yara-rules/index.yar "$CUR_ROOT/src" >/opt/result/tool-yara.txt 2>/opt/result/tool-yara.error
event stop tool-yara

LANGUAGES=()
[[ "$FILE_TYPES" =~ ( )(javascript|typescript)( ) ]] && LANGUAGES+=("javascript")
[[ "$FILE_TYPES" =~ ( )java( ) ]] && LANGUAGES+=("java")
[[ "$FILE_TYPES" =~ ( )(csharp|cs|c#|csproj)( ) ]] && LANGUAGES+=("csharp")
[[ "$FILE_TYPES" =~ ( )python( ) ]] && LANGUAGES+=("python")
[[ "$FILE_TYPES" =~ ( )(c|h|hpp|c\+\+|cpp)( ) ]] && LANGUAGES+=("cpp")
[[ "$FILE_TYPES" =~ ( )go( ) ]] && LANGUAGES+=("go")
[[ "$FILE_TYPES" =~ ( )ruby( ) ]] && LANGUAGES+=("ruby")

for LANGUAGE in "${LANGUAGES[@]}"; do
    QUERY_ROOT="/opt/codeql-queries"
    CODEQL_SUITES=("$QUERY_ROOT/$LANGUAGE/ql/src/codeql-suites/$LANGUAGE-security-extended.qls")

    if [ -f "$QUERY_ROOT/$LANGUAGE/ql/src/codeql-suites/solorigate.qls" ]; then
        CODEQL_SUITES+=("$QUERY_ROOT/$LANGUAGE/ql/src/codeql-suites/solorigate.qls")
    fi

    # Run CodeQL against the downloaded package (no installation)
    printf "${RED}Running CodeQL basic...(${LANGUAGE})${NC}\n"
    cd "$CUR_ROOT/src"
    NONVERSION_SCRIPT="${BUILD_SCRIPT_ROOT}/${PACKAGE_PURL_TYPE}/${PACKAGE_PURL_NAME}"
    VERSION_SCRIPT="${BUILD_SCRIPT_ROOT}/${PACKAGE_PURL_TYPE}/${PACKAGE_PURL_NAME}/${PACKAGE_PURL_VERSION}"
    if [ -f "${VERSION_SCRIPT}/Makefile" ]; then
        make -f "${VERSION_SCRIPT}/Makefile" >>/opt/result/tool-codeql-db-basic.log 2>&1
    elif [ -f "${NONVERSION_SCRIPT}/Makefile" ]; then
        make -f "${VERSION_SCRIPT}/Makefile" >>/opt/result/tool-codeql-db-basic.log 2>&1
    else
        echo "No build script found." >>/opt/result/tool-codeql-db-installed.log 2>&1
    fi

    cd "$CUR_ROOT"
    event start tool-codeql-basic-create
    if [ "$PACKAGE_PURL_TYPE" = "ubuntu" ]; then
        _UBUNTU_VERSION=$(apt show "$PACKAGE_PURL_NAME" 2>/dev/null | grep "$PACKAGE_PURL_VERSION" | grep Version: | cut -d" " -f2)
        mkdir "$CUR_ROOT/ubuntu-src"
        cd "$CUR_ROOT/ubuntu-src"
        apt source "$PACKAGE_PURL_NAME=$_UBUNTU_VERSION"
        _UBUNTU_SRC=$(find . -maxdepth 1 -type d | grep "$PACKAGE_PURL_NAME" | head -1 | xargs readlink -f)
        apt build-dep -y "$PACKAGE_PURL_NAME=$_UBUNTU_VERSION"
        timeout $LONG_ANALYZER_TIMEOUT codeql database create --language="$LANGUAGE" --source-root="$_UBUNTU_SRC" --threads=0 --command="debuild -b -uc -us" tool-codeql-db-basic.$LANGUAGE >>/opt/result/tool-codeql-db-basic.$LANGUAGE.log 2>&1
    else
        timeout $LONG_ANALYZER_TIMEOUT codeql database create --language="$LANGUAGE" --source-root="$CUR_ROOT/src" --threads=0 tool-codeql-db-basic.$LANGUAGE >>/opt/result/tool-codeql-db-basic.$LANGUAGE.log 2>&1
    fi

    if [ $? -eq 124 ]; then
        event stop tool-codeql-basic-create
        echo "CodeQL [create database] timed out after $LONG_ANALYZER_TIMEOUT." >>/opt/result/tool-codeql-db-basic.$LANGUAGE.error
    else
        event stop tool-codeql-basic-create
        codeql database upgrade tool-codeql-db-basic.$LANGUAGE >>/opt/result/tool-codeql-db-basic.$LANGUAGE.log 2>&1
        codeql database bundle tool-codeql-db-basic.$LANGUAGE --output /opt/result/tool-codeql-db-basic.$LANGUAGE.zip >>/opt/result/tool-codeql-db-basic.$LANGUAGE.log 2>&1
        event start tool-codeql-basic-analyze
        timeout "$LONG_ANALYZER_TIMEOUT" codeql database analyze --format=sarifv2.1.0 --additional-packs=/opt/codeql-queries/misc --output=/opt/result/tool-codeql-basic.$LANGUAGE.sarif --sarif-add-snippets --threads=0 tool-codeql-db-basic.$LANGUAGE ${CODEQL_SUITES[@]} 2>>/opt/result/tool-codeql-basic.$LANGUAGE.error >>/opt/result/tool-codeql-db-basic.$LANGUAGE.log
        if [ $? -eq 124 ]; then
            echo "CodeQL [analyze] timed out after $LONG_ANALYZER_TIMEOUT." >>/opt/result/tool-codeql-db-basic.$LANGUAGE.error
        else
            dos2unix /opt/result/tool-codeql-basic.$LANGUAGE.sarif >/dev/null 2>&1
        fi
    fi
    event stop tool-codeql-basic-analyze
done

# Install the package locally, and then run CodeQL again
for LANGUAGE in "${LANGUAGES[@]}"; do
    if [ "$PACKAGE_PURL_TYPE" == "npm" ]; then
        printf "${RED}Running CodeQL after install...${NC}\n"
        cd "${CUR_ROOT}/installed"

        event start tool-codeql-installed-install
        npm i "${PACKAGE_PURL_NAMESPACE_NAME}@${PACKAGE_PURL_VERSION}" >>/opt/result/tool-codeql-db-installed.log 2>&1
        event stop tool-codeql-installed-install

        # Don't ignore any files
        export LGTM_INDEX_FILTERS="include:**/*"

        cd "${CUR_ROOT}"
        event start tool-codeql-installed-create
        timeout $LONG_ANALYZER_TIMEOUT codeql database create --language="$LANGUAGE" --source-root="$CUR_ROOT/installed" --threads=0 tool-codeql-db-installed >>/opt/result/tool-codeql-db-installed.log 2>&1
        if [ $? -eq 124 ]; then
            event stop tool-codeql-installed-create
            echo "CodeQL [create database] timed out after $LONG_ANALYZER_TIMEOUT." >>/opt/result/tool-codeql-db-installed.error
        else
            event stop tool-codeql-installed-create
            # Normal Rules
            codeql database upgrade tool-codeql-db-installed >>/opt/result/tool-codeql-db-installed.log 2>&1
            codeql database bundle tool-codeql-db-installed --output /opt/result/tool-codeql-db-installed.zip >>/opt/result/tool-codeql-db-installed.log 2>&1
            event start tool-codeql-installed-analyze
            timeout "$LONG_ANALYZER_TIMEOUT" codeql database analyze --format=sarifv2.1.0 --additional-packs=/opt/codeql-queries/misc --output=/opt/result/tool-codeql-installed.sarif --sarif-add-snippets --threads=0 tool-codeql-db-installed ${CODEQL_SUITES[@]} 2>>/opt/result/tool-codeql-installed.error >>/opt/result/tool-codeql-db-installed.log
            if [ $? -eq 124 ]; then
                echo "CodeQL [analyze] timed out after $LONG_ANALYZER_TIMEOUT." >>/opt/result/tool-codeql-db-installed.error
            else
                dos2unix /opt/result/tool-codeql-installed.sarif >/dev/null 2>&1
            fi
            event stop tool-codeql-installed-analyze
        fi

        # Control Flow Analysis: Re-use the installed database
        if [ -f "/opt/toolshed/etc/codeql-controlflow-$LANGUAGE.template" ]; then
            CODEQL_CONTROLFLOW_QUERY="/opt/codeql-queries/$LANGUAGE/ql/src/controlflow-query.ql"
            mkdir -p $(dirname ${CODEQL_CONTROLFLOW_QUERY})
            sed "s|_SOURCE_|$PACKAGE_PURL_NAME|gi" /opt/toolshed/etc/codeql-controlflow-$LANGUAGE.template >"$CODEQL_CONTROLFLOW_QUERY"

            # Write the qlpack.yml file
            echo "name: custom-controlflow-$LANGUAGE" >/opt/codeql-queries/$LANGUAGE/ql/qlpack.yml
            echo "version: 0.0.0" >>/opt/codeql-queries/$LANGUAGE/ql/qlpack.yml
            echo "libraryPathDependencies: codeql-$LANGUAGE" >>/opt/codeql-queries/$LANGUAGE/ql/qlpack.yml
        else
            printf "${BG_RED}${WHITE}Missing CodeQL control flow template for ${LANGUAGE}.${NC}\n"
        fi

        printf "${RED}Running CodeQL control flow analysis...${NC}\n"
        cd "${CUR_ROOT}"
        event start tool-codeql-installed-codeflow-analyze
        codeql query run --database tool-codeql-db-installed --output=/opt/result/tool-codeql-db-installed-codeflow.bqrs "$CODEQL_CONTROLFLOW_QUERY" >/opt/result/tool-codeql-db-installed-codeflow.log 2>/opt/result/tool-codeql-db-installed-codeflow.error
        codeql bqrs info /opt/result/tool-codeql-db-installed-codeflow.bqrs >>/opt/result/tool-codeql-db-installed-codeflow.log 2>>/opt/result/tool-codeql-db-installed-codeflow.error
        codeql bqrs decode --format=csv --no-titles --output=/opt/result/tool-codeql-db-installed-codeflow.csv --result-set=#select /opt/result/tool-codeql-db-installed-codeflow.bqrs >>/opt/result/tool-codeql-db-installed-codeflow.log 2>>/opt/result/tool-codeql-db-installed-codeflow.error
        # Cut the sinks out of the CSV file (taking into account NPM scopes)
        if [ -f "/opt/result/tool-codeql-db-installed-codeflow.csv" ]; then
            csvtool col 3 /opt/result/tool-codeql-db-installed-codeflow.csv |
                grep -Eo 'node_modules/([^/]+|@[^/]+\/[^/]+)/' |
                sed 's/^node_modules\///' |
                sed 's/\/$//' |
                sed 's/@/%40/g' |
                sed 's/\//%2F/g' |
                sed 's/^/pkg:npm\//g' |
                sort |
                uniq > /opt/result/tool-codeql-db-installed-codeflow-sinks.txt
        else
            echo "Unable to generate control flow graph." >/opt/result/tool-codeql-db-installed-codeflow.error
        fi
        event stop tool-codeql-installed-codeflow-analyze
    fi
done

# Trace syscalls during installation
printf "${RED}Checking syscalls during installation...${NC}\n"
rm -rf "$CUR_ROOT/installed_syscall" && mkdir -p "$CUR_ROOT/installed_syscall" && cd "$CUR_ROOT/installed_syscall"
event start tool-strace
if [ "$PACKAGE_PURL_TYPE" == "npm" ]; then
    strace -f -ff -e trace=network,file,process -s 128 -D -o /opt/result/tool-strace.javascript.txt npm i "$PACKAGE_PURL_NAMESPACE_NAME@$PACKAGE_PURL_VERSION" >/opt/result/tool-strace.log 2>&1
elif [ "$PACKAGE_PURL_TYPE" == "pypi" ]; then
    strace -f -ff -e trace=network,file,process -s 128 -D -o /opt/result/tool-strace.python.txt pip3 install --no-compile --root /tmp/pip-build-temp "$PACKAGE_PURL_NAME==$PACKAGE_PURL_VERSION" >/opt/result/tool-strace.log 2>&1
    rm -rf /tmp/pip-build-temp
elif [ "$PACKAGE_PURL_TYPE" == "nuget" ]; then
    dotnet new console -o /tmp/nuget-build-temp >/opt/result/tool-strace.log 2>&1
    strace -f -ff -e trace=network,file,process -s 128 -D -o /opt/result/tool-strace.csharp.txt dotnet add /tmp/nuget-build-temp package "$PACKAGE_PURL_NAME" --version "$PACKAGE_PURL_VERSION" >/opt/result/tool-strace.log 2>&1
    rm -rf /tmp/nuget-build-temp
fi
if [ -n "$(ls -A /opt/result/tool-strace.*.txt.* 2>/dev/null)" ]; then
    cat /opt/result/tool-strace.*.txt.* >/opt/result/tool-strace.txt
    rm /opt/result/tool-strace.*.txt.*
fi
event stop tool-strace

# NPM Audit
if [ "$PACKAGE_PURL_TYPE" == "npm" ]; then
    printf "${RED}Checking NPM Audit...${NC}\n"
    rm -rf "$CUR_ROOT/installed" && mkdir -p "$CUR_ROOT/installed" && cd "$CUR_ROOT/installed"
    event start tool-npm-audit
    npm init -y >/opt/result/tool-npm-audit.log 2>&1
    npm i "$PACKAGE_PURL_NAMESPACE_NAME@$PACKAGE_PURL_VERSION" >>/opt/result/tool-npm-audit.log 2>&1
    npm audit --json >/opt/result/tool-npm-audit.json 2>>/opt/result/tool-npm-audit.log
    event stop tool-npm-audit
fi

# Manalyze - https://github.com/JusticeRage/Manalyze
printf "${RED}Checking Manalyze...${NC}\n"
event start tool-manalyze
find "$CUR_ROOT/src" -type f -print0 | xargs -0 file | grep "PE32" | cut -d: -f1 | xargs -I{} -n1 bash -c 'F="{}"; FN=$(echo $F | shasum -a256 | cut -d" " -f1); manalyze -d all --plugins=compilers,peid,strings,findcrypt,packer,imports,resources,mitigation,overlay,authenticode -o json --pe "$F" >"/opt/result/tool-manalyze.$FN.json" 2>>/opt/result/tool-manalyze.log'
if [ -n "$(ls -A /opt/result/tool-manalyze.*.json 2>/dev/null)" ]; then
    cat /opt/result/tool-manalyze.*.json | jq -s > /opt/result/tool-manalyze.json
    rm /opt/result/tool-manalyze.*.json
fi
event stop tool-manalyze

printf "${BLUE}Post-processing...${NC}\n"
event start post-process
python /opt/toolshed/postprocess.py "$PACKAGE_PURL" /opt/result/
event stop post-process

printf "${BLUE}Copying results to ${EXPORT_DIR}...${NC}\n"
event start export-dir
cp -R /opt/result/* "$EXPORT_DIR"
event stop export-dir

STOP_TIME=$(date +%s)
(( DURATION = STOP_TIME - START_TIME ))
printf "${BLUE}Operation completed in ${YELLOW}${DURATION}${BLUE} seconds.${NC}\n\n"

printf "${BLUE}Analysis Summary: ${DARKGRAY}[ ${YELLOW}"
printf "%s" "${PACKAGE_PURL}"
printf "${DARKGRAY}]${NC}\n${BLUE}"
printf -- "-%.0s" $(seq 1 $(( 21 + ${#PACKAGE_PURL} )))
printf "\n${NC}${DARKGRAY}"
if [ -f /opt/result/summary-console.txt ]; then
    cat /opt/result/summary-console.txt | sort | uniq
fi
printf "${NC}\n\n"

event stop runtools

cp /tmp/events.txt "$EXPORT_DIR/summary-telemetry-events.txt"

exit 0