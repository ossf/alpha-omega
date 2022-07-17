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

## Running

To run the image, navigate to the `worker` directory and run the `run-analysis.ps1`
script with relevant parameters:

```powershell
run-analysis.ps1 -PackageUrl "pkg:npm/left-pad@1.3.0"
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
