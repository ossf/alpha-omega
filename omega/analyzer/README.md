# Omega Analyzer

The Omega Analyzer is a self-contained container image that has a broad set of security tools
preinstalled, along with an orchestration script to run those tools against a target and
aggregate the results.

While it can be used interactively, it's primary purpose is to be run from the host, with
output send to a mapped directory.

## Building

To build the container image, just run `build.ps1` or `docker build` with your
chosen tag, from this directory. The build script contains cache burst parameter,
pass in `-Force` to `build.ps1` to re-build all layers.

**This will take a long time.** As part of the build, we download CodeQL and pre-compile
all queries (to make later analysis faster). This can take up to a few hours on typical
hardware.

We're exploring making the pre-built image available.

Alternatively, can use the following command to build from docker

```sh
docker build -t openssf/omega-toolshed:$(grep -E '^LABEL version.*' Dockerfile | cut -d= -f2 | tr -d '"') . -f Dockerfile

# The command `$(grep -E '^LABEL version.*' Dockerfile | cut -d= -f2 | tr -d '"')` is responsible for searching for the version number on the Dockerfile and using that as the tag on Docker
```

### Troubleshooting steps

#### MacOS M1 Chip
If using a Mac OSX with the latest Docker Desktop (4.15 as of writing), `docker build build.ps1` will shoot out several error messages.

Make sure to create `/etc/apt/` with sudo user

Download and install
* `wget` with `brew install wget`
* `dkpg` with `brew install dpkg`
* .NET core with `brew install mono-libgdiplus`

There is a known issue with [M1 Apple chip on MacOS](https://stackoverflow.com/questions/71040681/qemu-x86-64-could-not-open-lib64-ld-linux-x86-64-so-2-no-such-file-or-direc), which would produce the error when running

```qemu-x86_64: Could not open '/lib64/ld-linux-x86-64.so.2': No such file or directory```

The following two options are available to work around this issue:
1. Set the DOCKER_DEFAULT_PLATFORM environment variable to linux/amd64

`export DOCKER_DEFAULT_PLATFORM=linux/amd64`
2. In the FROM section of the Dockerfile, line 1, modify to the following

`FROM --platform=linux/amd64 mcr.microsoft.com/mirror/docker/library/ubuntu:22.04`

## Running

To run the image, navigate to the `worker` directory and run the `run-analysis-complete.ps1`
script with relevant parameters:

```powershell
run-analysis-complete.ps1 -PackageUrl "pkg:npm/left-pad@1.3.0"
                 -PreviousVersion "1.2.0"
                 -OutputDirectoryName "output"
```

The result will be a directory containing all output files from the analysis placed into
a subdirectory within `output` and if the results were "clean", a security review placed
in `security-reviews`.

You can also run the image directly (which will not include reproducibility or a security review):

```sh
docker run --rm -it --mount type=bind,source=/tmp/output_dir,target=/opt/export openssf/omega-toolshed:latest pkg:npm/left-pad@1.3.0 1.2.0
```

### Standalone

To run this as a standalone from a **built** image, run the following:

```sh
# Template of command
docker run --rm -v <LOCAL_COMPUTER_DIR>:/opt/export/<PKG_DIR> --env-file .env openssf/omega-toolshed:latest pkg:<PKG_FORMAT>
```

```sh
# Example of command
docker run --rm -v ./npm/left-pad/:/opt/export/npm/left-pad/1.3.0 --env-file .env openssf/omega-toolshed:latest pkg:npm/left-pad@1.3.0
```
The result will be a directory containing all output files from the analysis placed into
a directory on your local machine (not the container) in `./npm/left-pad`. 

An example of the [.env](./worker/.env.example) should contain `librariesIO` api key to get the packages from the net. Simply create an account on libraries IO to get the API key.

<!--
```sh
# For some extra hacking on the container, use this
docker run --rm --entrypoint /bin/bash --env-file .env openssf/omega-toolshed:latest pkg:<PKG_FORMAT>
```
-->


## License

The Omega Analyzer scripts and all content that resides within this repository are licensed
under the [Apache](../../LICENSE) license. However, the [Dockerfile](Dockerfile) downloads
and installs other tools that are provided under separate licenses; for example:

* [CodeQL](https://codeql.github.com/) is provided under a 
  [custom license](https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md), which
  you should understand before using this analyzer.
* [Radare2](https://rada.re/) is provided under the
  [LGPLv3 license](https://rada.re/r/license.html).

Please refer to the [Dockerfile](Dockerfile) for more information about the varying licenses
of the included tools and any restrictions that may apply to their use. In particular, ensure
you understand the
[restrictions for CodeQL](https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md).
