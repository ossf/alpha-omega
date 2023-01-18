## Omega

The purpose of Omega is to run leading-edge security analysis against the top 10,000 (or more)
open source projects, to validate and triage those findings, and then to get the issues fixed
by working with project maintainers.

### Analysis Toolchain

Omega uses a publicly available toolchain, which consists of dozens of open source and freely-
available tools. These tools include CodeQL, Semgrep, OSS Gadget, and others. For a full list
of analyzers, please see [list-of-tools](analyzer/list-of-tools.md).

To run the Omega analysis toolchain, please see [analyzer](analyzer/README.md).

### Omega Assertion Framework

Omega provides a set of tools for generating assertions and executing policies against them.
For more information, see [OAF](oaf/README.md).