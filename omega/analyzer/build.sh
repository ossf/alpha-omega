#!/bin/bash

OPT_FORCE=

# usage: shows how to use this script
function usage {
cat<<EOF
    $0 -[h|f]

       -h : Help
       	  Shows the usage of the program

       -f : Force
       	  Force build of the container

EOF
exit 0
}

function main {
    { # try
	version=$(grep -E '^LABEL version.*' Dockerfile | cut -d= -f2 | tr -d '"')

	if [ $OPT_FORCE ]; then
	    docker build -t openssf/omega-toolshed:$version . -f Dockerfile --build-arg CACHEBUST=$(date '+%FT%T.%N%:z')
	else
	    docker build -t openssf/omega-toolshed:$version . -f Dockerfile
	fi
	docker tag openssf/omega-toolshed:$version openssf/omega-toolshed:latest
	
    } || { #catch
	echo "Error running build."
    }
}

while getopts 'hf' opt; do
    case "$opt" in
	# h) help
       	h) usage;;
	# f) Force
	f) OPT_FORCE=1;;
    esac
done

main
