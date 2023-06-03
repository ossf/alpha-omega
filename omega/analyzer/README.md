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

#### Docker Issues
<details>
	<summary>failed to create endpoint ([A-Za-z0-9]+) on network bridge: failed to add the host ([A-Za-z0-9]+) <=> sandbox ([A-Za-z0-9]+) pair interfaces: operation not supported </summary>

- Beware of kernel issues if you have a rolling-release distro, it would be prudent to `reboot system` and restart the `docker` service

- If those don't work check the Resoures below

##### Resources
- https://github.com/moby/moby/issues/27426
	
</details>


<details>
	<summary>semgrep rules syntax error</summary>

- Sometimes an error will be thrown for specific areas in semgrep, to solve this fix the following semgrep area:

```Dockerfile
# R2C Semgrep (with many rules)
# License: LGPLv2.1 - https://github.com/returntocorp/semgrep/blob/develop/LICENSE
RUN mkdir /opt/semgrep-rules && \
    cd /opt/semgrep-rules && \
    wget -O auto.yml https://semgrep.dev/c/p/auto && \
    wget -O brakeman.yml https://semgrep.dev/c/p/brakeman && \
#    wget -O ci.yml https://semgrep.dev/c/p/ci && \
    wget -O clientside-js.yml https://semgrep.dev/c/p/clientside-js && \
    wget -O command-injection.yml https://semgrep.dev/c/p/command-injection && \
#    wget -O default.yml https://semgrep.dev/c/p/default && \
    wget -O django.yml https://semgrep.dev/c/p/django && \
    wget -O docker-compose.yml https://semgrep.dev/c/p/docker-compose && \
    wget -O docker.yml https://semgrep.dev/c/p/docker && \
    wget -O dockerfile.yml https://semgrep.dev/c/p/dockerfile && \
    wget -O electron-desktop-app.yml https://semgrep.dev/c/p/electron-desktop-app && \
    wget -O eslint-plugin-security.yml https://semgrep.dev/c/p/eslint-plugin-security && \
    wget -O expressjs.yml https://semgrep.dev/c/p/expressjs && \
    wget -O flask.yml https://semgrep.dev/c/p/flask && \
    wget -O github-actions.yml https://semgrep.dev/c/p/github-actions && \
    wget -O gitlab-bandit.yml https://semgrep.dev/c/p/gitlab-bandit && \
    wget -O gitlab-eslint.yml https://semgrep.dev/c/p/gitlab-eslint && \
    wget -O golang.yml https://semgrep.dev/c/p/golang && \
    wget -O insecure-transport.yml https://semgrep.dev/c/p/insecure-transport && \
    wget -O java.yml https://semgrep.dev/c/p/java && \
    wget -O javascript.yml https://semgrep.dev/c/p/javascript && \
    wget -O jwt.yml https://semgrep.dev/c/p/jwt && \
    wget -O kubernetes.yml https://semgrep.dev/c/p/kubernetes && \
    wget -O mobsfscan.yml https://semgrep.dev/c/p/mobsfscan && \
    wget -O nginx.yml https://semgrep.dev/c/p/nginx && \
    wget -O nodejs.yml https://semgrep.dev/c/p/nodejs && \
    wget -O nodejsscan.yml https://semgrep.dev/c/p/nodejsscan && \
    wget -O ocaml.yml https://semgrep.dev/c/p/ocaml && \
#    wget -O owasp-top-ten.yml https://semgrep.dev/c/p/owasp-top-ten && \
    wget -O phpcs-security-audit.yml https://semgrep.dev/c/p/phpcs-security-audit && \
#    wget -O python.yml https://semgrep.dev/c/p/python && \
    wget -O r2c-best-practices.yml https://semgrep.dev/c/p/r2c-best-practices && \
#    wget -O r2c-bug-scan.yml https://semgrep.dev/c/p/r2c-bug-scan && \
#    wget -O r2c-ci.yml https://semgrep.dev/c/p/r2c-ci && \
#    wget -O r2c-security-audit.yml https://semgrep.dev/c/p/r2c-security-audit && \
#    wget -O r2c.yml https://semgrep.dev/c/p/r2c && \
    wget -O react.yml https://semgrep.dev/c/p/react && \
    wget -O ruby.yml https://semgrep.dev/c/p/ruby && \
    wget -O secrets.yml https://semgrep.dev/c/p/secrets && \
    wget -O semgrep-misconfigurations.yml https://semgrep.dev/c/p/semgrep-misconfigurations && \
    wget -O semgrep-rule-lints.yml https://semgrep.dev/c/p/semgrep-rule-lints && \
    wget -O sql-injection.yml https://semgrep.dev/c/p/sql-injection && \
    wget -O supply-chain.yml https://semgrep.dev/c/p/supply-chain && \
    wget -O terraform.yml https://semgrep.dev/c/p/terraform && \
    wget -O test.yml https://semgrep.dev/c/p/test && \
    wget -O trailofbits.yml https://semgrep.dev/c/p/trailofbits && \
    wget -O typescript.yml https://semgrep.dev/c/p/typescript && \
    wget -O xss.yml https://semgrep.dev/c/p/xss && \
    wget -O gitlab-gosec.yml https://semgrep.dev/c/r/gitlab.gosec && \
    wget -O hazanasec.weak_crypto.yml https://semgrep.dev/c/p/hazanasec.weak_crypto && \
    wget -O hazanasec.non-prepared-sql-statements.yml https://semgrep.dev/c/p/hazanasec.non-prepared-sql-statements && \
    wget -O hazanasec.nodejs_nosql_injection.yml https://semgrep.dev/c/p/hazanasec.nodejs_nosql_injection && \
    wget -O hazanasec.jwt-security-audit.yml https://semgrep.dev/c/p/hazanasec.jwt-security-audit && \
    wget -O hazanasec.generic_possible_xss.yml https://semgrep.dev/c/p/hazanasec.generic_possible_xss && \
    wget -O hazanasec.possible_path_traversal.yml https://semgrep.dev/c/p/hazanasec.possible_path_traversal && \
    wget -O findsecbugs.yml https://semgrep.dev/c/p/findsecbugs && \
    wget -O webappsecurityz.3zrr-rules.yml https://semgrep.dev/c/p/webappsecurityz.3zrr-rules && \
    wget -O traw.c.yml https://semgrep.dev/c/p/traw.c && \
    wget -O tkisason.javascript-kitchensink.yml https://semgrep.dev/c/p/tkisason.javascript-kitchensink && \
    semgrep -f /opt/semgrep-rules --validate --metrics=off
```

</details>

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
