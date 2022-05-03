# Omega Analyzer

The Omega Analyzer consists of a Docker container with a suite of security
tools pre-installed, along with scripts to orchestrate their execution
against an open source package.

## Building

To build the container image, just run `build.ps1` or `docker build` with your
chosen tag, from this directory. The build script contains cache burst parameter,
pass in `-Force` to re-build all layers.

## Running

To run the image, navigate to the `worker` directory and run the `run-analysis.ps1`
script with relevant parameters:

```powershell
run-analysis.ps1 -PackageUrl "pkg:npm/left-pad@1.3.0"
                 -PreviousVersion "1.2.0"
                 -OutputDirectoryName "output"
```

The result will be a directory containing all output files from the analysis placed into
a subdirectory within `output` and a security review placed in `security-reviews`.

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
of the included applications.
