## We’ve decided to end the Omega engineering project. The project’s mission was to build the tools and processes for conducting automated campaigns that discover, triage, and remediate security findings to significantly reduce the presence of security vulnerabilities, at scale, from the Open Source Software ecosystem. The team was made up of one engineer and one security researcher. The initial goals were to validate the vision and to build an MVP.  The team did excellent work and we learned a lot. Two specific factors were significant contributors to this decision: It became very clear that Alpha-Omega is not set up to be an engineering organization. There are staffing and operational overheads that do not fit our organizational structure. It also became apparent that this would become a large project that would exceed Alpha-Omega’s funding. In any large effort, strategy comes down to priorities. We decided that the short and medium term ROI of this work did not match the other important work that Alpha-Omega is doing. The overall mission of Alpha-Omega hasn’t changed, nor has our desire to fix the most critical projects and ecosystem while also scaling solutions for “the rest” of the open source community. All of the source code work is open source and is available for anyone to use.


[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7115/badge)](https://bestpractices.coreinfrastructure.org/projects/7115)

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
