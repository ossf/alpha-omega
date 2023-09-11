#!/bin/bash
#
# This will create a copy with more verbosity on the package-name
# It also the POC for Bulk Scanning
#
# v1.0 Andres Orbe

OUT_DIR=./out
LOCAL_SAVE=./output
PKG_MANAGER=
SKIP_PARTNER=1
JUST_SHOW=
ENV_FILE=
SEQUE="1,2"

# usage: describes usage / help of the $0
function usage() {
cat <<EOF
    $0 - Bulk Scan Script for Analyzer

- Requires '-e "Location of an environment variable" '
EOF
}

# handle flags / program arguments
while getopts "p:sq:je:h" opt; do
    case "${opt}" in
	p) PKG_MANAGER="${OPTARG}";;
	s) SKIP_PARTNER=0;;
	q) SEQUE="${OPTARG}";;
	j) JUST_SHOW=1;;
	e) ENV_FILE="${OPTARG}";;
	h) usage && exit 0;;
    esac
done


# 'Default' Setting
[ -s $PKG_MANAGER ] && PKG_MANAGER="pypi" # this defaults search to be pypi, if not set
[ ! -z $JUST_SHOW ] && awk -F ',' '{if (match($1,/pypi|maven|npm/,m)) printf "%s/%s\n", $1, $2}' ./omega-top10k.csv | grep -E "^${PKG_MANAGER}" | sed -n "${SEQUE}p" && exit 0



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

if [ $SKIP_PARTNER -eq 1 ]; then    
    for pkg in `awk -F ',' '{if (match($1,/pypi|maven|npm/,m)) printf "%s/%s\n", $1, $2}' ./omega-top10k.csv | grep -E "^${PKG_MANAGER}" | sed -n "${SEQUE}p"`; do
	echo "pkg:${pkg}@latest"

    echo $pkg
        mkdir -p "${LOCAL_SAVE}"
	docker run --env-file $ENV_FILE -v $LOCAL_SAVE:/opt/export --rm -it openssf/omega-toolshed:latest "pkg:${pkg}@latest"
	resultsGrab "${pkg}"
	teleGrab "${pkg}"
    done
fi
