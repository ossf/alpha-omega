# Alpha Engagement: OpenRefactory

OpenRefactory thanks Alpha-Omega for supporting the project to generate VEX documents at scale.

OpenRefactory will work with Piotr Karwasz of Apache Software Foundation to unlock the capability to generate VEX documents for Java packages. The source codes released are all available under the following GitHub organization: [VEX Generation Toolset](https://github.com/vex-generation-toolset/).

The project started from July 2025 and will end at December 2025.

## Use Cases

* As a project maintainer I can triage and review newly discovered vulnerabilities in my project’s supply chain.
* As a project maintainer I can use static analysis tools to determine the reachable vulnerabilities in my project’s supply chain.
* As a project maintainer I can see the callgraphs of reachable vulnerabilities in my project’s supply chain. I can also see which vulnerabilities are not reachable by my project.
* As a project maintainer I can automatically generate and then manually review and edit mini VEX statements for all vulnerabilities in my supply chain. 
* As a project maintainer I can periodically create an updated VEX document that reflects the automatic and manual analysis of risk for all vulnerabilities in my project’s supply chain

## Deliverables
All deliverables are to be open source.

### Java callgraph generator

* Derived from existing OpenRefactory implementation
* Creates a callgraph compatible with the capslock format

### Root Cause Servcie

* Vulnerability to source mapper
* Scoped to a specific package version and vulnerability
* Identifies vulnerable lines of code
* Can default to all lines of code when the package is small or if there are too many ambiguities
* Optimizes for reducing false negatives
* Persists in a text file suitable for ingestion by other tools (e.g. MyPackage-CVE1234-vulnerable-lines.txt) and for persistence and review in a source repo.
Covers Java and at least one other mainstream language (e.g. JavaScript, Python, ...)

### Vulnerability reachability analysis

* Scoped to a specific package version and SBOM for that version
* Produces call graph traces for reachable vulnerabilities
* Produces a textual explanation of the vulnerability reachability
* Produces a vexplanation.txt file suitable for human edit, review, and persistence in a source repo
* Re-uses prior vexplanation.txt files when re-invoked.

### VEX statement generator

* Scoped to a specific package version.
* Compiles multiple vexplanation.txt files into a VEX statement for the package version

### Explain-the-vulnerability/ VEXplanation generator tool

* A tool to visualize the results from the previous tools, making them more accessible to developers.

### VEX Workflow tool

* Scoped to a specific package version and SBOM for that version
* Enumerates vulnerabilities from the SBOM and invokes per-vulnerability reachability analysis
* Defines a path and repo based convention for organizing and caching output from various tools
* Supports fully-automated batch execution.

## Timeline

This engagement started in July 2025. The engagement ended in December 2025.

## Monthly Updates

* [July 2025](update-2025-07.md)
* [August 2025](update-2025-08.md)
* [September 2025](update-2025-09.md)
* [October 2025](update-2025-10.md)
* [November 2025](update-2025-11.md)

## Primary Contacts

* Munawar Hafiz - CEO, OpenRefactory
* Piotr Karwasz - Apache Software Foundation

