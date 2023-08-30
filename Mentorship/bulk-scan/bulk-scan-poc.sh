#!/bin/bash
#
# This will create a copy with more verbosity on the package-name
# It also the POC for Bulk Scanning
#
# v1.0 Andres Orbe

OUT_DIR=./out
LOCAL_SAVE=./output
HEAD_COUNT=
PKG_MANAGER=
SKIP_PARTNER=1
TAIL_COUNT=
JUST_SHOW=
ENV_FILE=
SEQUE="1,2"


while getopts "n:p:t:sq:je:" opt; do
    case "${opt}" in
	n) HEAD_COUNT="${OPTARG}";;
	p) PKG_MANAGER="${OPTARG}";;
	t) TAIL_COUNT="${OPTARG}";;
	s) SKIP_PARTNER=0;;
	q) SEQUE="${OPTARG}";;
	j) JUST_SHOW=1;;
	e) ENV_FILE="${OPTARG}":
    esac
done

[ -s $HEAD_COUNT ] && HEAD_COUNT=10
[ -s $TAIL_COUNT ] && TAIL_COUNT=$(( $HEAD_COUNT + 10 ))
[ -s $PKG_MANAGER ] && PKG_MANAGER="pypi"
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

	# echo "###DEBUG: teleGrab [result]   --> [$result]"
	# echo "###DEBUG: teleGrab [cpy_path] --> [$cpy_path]"
	# echo "###DEBUG: teleGrab [save_all] --> [$save_all]"


	mkdir -p ${OUT_DIR}
	[ ! -s "${save_all}" ] && cp $result $save_all	

	# cp $result $cpy_path
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
