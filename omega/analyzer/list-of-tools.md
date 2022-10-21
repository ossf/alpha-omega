# Tools Used in the Omega Analyzer

We use the following tools within the Omega Analyzer (in no particular order):

* [DevSkim](https://github.com/Microsoft/DevSkim)
* [NodeJsScan](https://github.com/ajinabraham/nodejsscan)
* [CppCheck](https://github.com/danmar/cppcheck)
* [Radare2](https://rada.re)
* [CodeQL](https://github.com/github/codeql-cli-binaries)
* [Lizard](https://github.com/terryyin/lizard)
* [ShhGit](https://github.com/eth0izzle/shhgit)
* [SecretScanner](https://github.com/deepfence/SecretScanner)
* [Detect-Secrets](https://github.com/Yelp/detect-secrets)
* [SCC](https://github.com/boyter/scc)
* [Brakeman](https://github.com/presidentbeef/brakeman.git)
* [Graudit](https://github.com/wireghoul/graudit)
* [Application Inspector](https://github.com/microsoft/ApplicationInspector)
* [Manalyze](https://github.com/JusticeRage/Manalyze.git)
* [binwalk](https://manpages.ubuntu.com/manpages/bionic/en/man1/binwalk.1.html)
* [ClamAV](https://www.clamav.net/)
* [Bandit](https://bandit.readthedocs.io/en/latest/)
* [Semgrep](https://www.semgrep.dev/) with [many rules](https://github.com/ossf/alpha-omega/blob/main/omega/analyzer/Dockerfile#L294)
* [Yara](#) with [many rules](https://github.com/Yara-Rules/rules)
* [tbv](https://github.com/verifynpm/tbv)
* [ILSpy](https://github.com/icsharpcode/ILSpy)
* [strace](https://man7.org/linux/man-pages/man1/strace.1.html)
* [OSS Gadget](https://github.com/Microsoft/OSSGadget) (oss-download, oss-detect-cryptography, oss-detect-backdoor, oss-defog, oss-find-source)
* [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit)
* [Snyk Code](https://snyk.io)

You can view these tools within the Dockerfile and/or the [runtools.sh](worker/tools/runtools.sh) script.
