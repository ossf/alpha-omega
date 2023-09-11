#!/bin/bash
#
# This will create a copy with more verbosity on the package-name
# It also the POC for Bulk Scanning
#
# v1.0 Andres Orbe
tabs 4

# OUT_DIR: where the telemetry and results file is safely stored, think SHORTLIST 
OUT_DIR=./out

# LOCAL_SAVE: where the entire scan is stored, volatile because of mounting with container
LOCAL_SAVE=./output

PKG_MANAGER=
JUST_SHOW=
ENV_FILE=
SEQUE=

# usage: describes usage / help of the $0
function usage() {
cat <<EOF
    $0 - Bulk Scan Script for Analyzer

OPTIONS: -[$(cat $0 | grep -E '^while getopts' | grep -o '".*"' | sed -E 's/:|"//g' | sed -E 's/([A-Za-z0-9])/\1|/g' | rev | cut -c 1 --complement | rev)]

$(cat $0 | awk '/^while getopts/,/done/' | awk '/case/,/esac/' | grep -E '\s*#.*' | sed 's/\s*#/  -/g')

EXAMPLES:

$ $0 -e .env
- Runs bulk-scan script with .env in local directory

$ $0 -e .env -q 99
- Runs bulk-scan script at line 99

$ $0 -e .env -q 43,60
- Runs bulk-script with custom sequence lines 43 to 60 inclusive

$ $0 -d -q 34,45
- Dry-runs (doesn't actually perform a scan), used to check the packages you are going to scan before executing

NOTES:

- Requires '-e "Location of an environment variable"' to perform a scan (easier than running from local)
- Be sure to take 'omega-top10k.csv' with you!
EOF
}

# handle flags / program arguments
while getopts "p:q:de:h" opt; do
    case "${opt}" in
	# p: Package Manager - Select Package Manager
	p) PKG_MANAGER="${OPTARG}";;
	# q: seQuence - Choose awk sequence
	q) SEQUE="${OPTARG}";;
	# d: Dry-run - See which packages you are going to bulk-scan before doing it
	d) JUST_SHOW=1;;
	# e: Env file - Pass in .env file
	e) ENV_FILE="${OPTARG}";;
	# h: Help - Show Usage of Program
	h) usage && exit 0;;
    esac
done


# 'Default' Setting
[ -s $PKG_MANAGER ] && PKG_MANAGER="pypi" 
[ -s $SEQUE ] && SEQUE="1,2"

# This 
[ ! -z $JUST_SHOW ] && awk -F ',' '{if (match($1,/pypi|maven|npm/,m)) printf "%s/%s\n", $1, $2}' ./omega-top10k.csv | grep -E "^${PKG_MANAGER}" | sed -n "${SEQUE}p" && exit 0

# This program ($0) relies heavily on librariesIO API to get content
[ -z $ENV_FILE ] && echo "could not find .env with librariesIO key" && exit 1

# resultsGrab: grabs the 'summary-results.sarif' scan
function resultsGrab() {
    STACK_LOCAL_PATH="${1,,}"
    
    for result in `find $LOCAL_SAVE/$STACK_LOCAL_PATH -name 'summary-results.sarif'`; do

	pkg_man=$(echo $STACK_LOCAL_PATH | cut -d'/' -f1)
	pkg_nam=$(echo $STACK_LOCAL_PATH | cut -d'/' -f2)	
	ver_num=$(echo $result | rev | cut -d'/' -f1 --complement | cut -d'/' -f1 | rev)
	path=$(echo $result | rev | cut --complement -d'/' -f1 | rev)

	filename="$pkg_man-$pkg_nam-$ver_num-summary-results.sarif"
	cpy_path="$path/$pkg_man-$pkg_nam-$ver_num-summary-results.sarif"
	save_all="${OUT_DIR}/${filename}"

	mkdir -p ${OUT_DIR}
	[ ! -s "${save_all}" ] && cp $result $save_all

    done
}

# teleGrab: grab the 'telemetry-events.txt' file from the scan
function teleGrab() {
    STACK_LOCAL_PATH="${1,,}"
    for result in `find $LOCAL_SAVE/$STACK_LOCAL_PATH -name 'summary-telemetry-events.txt'`; do
	pkg_man=$(echo $STACK_LOCAL_PATH | cut -d'/' -f1)
	pkg_nam=$(echo $STACK_LOCAL_PATH | cut -d'/' -f2)	
	ver_num=$(echo $result | rev | cut -d'/' -f1 --complement | cut -d'/' -f1 | rev)
	path=$(echo $result | rev | cut --complement -d'/' -f1 | rev)
	
	filename="$pkg_man-$pkg_nam-$ver_num-summary-telemetry-events.txt"
	cpy_path="$path/$pkg_man-$pkg_nam-$ver_num-summary-telemetry-events.txt"
	save_all="${OUT_DIR}/${filename}"

	mkdir -p ${OUT_DIR}
	[ ! -s "${save_all}" ] && cp $result $save_all	
    done
}

for pkg in `awk -F ',' '{if (match($1,/pypi|maven|npm/,m)) printf "%s/%s\n", $1, $2}' ./omega-top10k.csv | grep -E "^${PKG_MANAGER}" | sed -n "${SEQUE}p"`; do
    echo "pkg:${pkg}@latest"
    echo $pkg

    mkdir -p "${LOCAL_SAVE}"

    # Must build the omega analyzer before-hand
    docker run --env-file $ENV_FILE -v $LOCAL_SAVE:/opt/export --rm -it openssf/omega-toolshed:latest "pkg:${pkg}@latest"

    # Both {results,tele}Grab require pkg.
    # $pkg Ex. pypi/amqp or pypi/attrs
    # no need for adding version number, (it will default and make it the latest pacakge available.)
    
    resultsGrab "${pkg}"
    teleGrab "${pkg}"
done

