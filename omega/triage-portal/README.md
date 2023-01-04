# Omega Triage Portal

The Omega Triage Portal is a web-application that can help manage automated vulnerability reports.
It was designed for scale, (hundreds of thousands of projects, many millions of findings),
but may also be useful at lower scale.

**The Portal is in early development, and is not ready for general use.**

## Getting Started

This extension can be used from GitHub Codespaces:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?machine=basicLinux32gb&repo=426394209&ref=scovetta%2Fadd-triage-portal&location=WestUs2&devcontainer_path=.devcontainer%2Ftriage-portal%2Fdevcontainer.json)

Once loaded, open the `.vscode/project.code-workspace` file and then click the `Open Workspace`
button. A new widow will open. This is needed because VS Code launch settings are nested
within the omega/triage-portal folder.

You can then run the Django launch task to start the application. Navigate to
<http://localhost:8001/admin> and enter the default credentials (admin/admin), then
navigate back to <http://localhost:8001>.

## Contributing

TBD

## Security

See [SECURITY.md](https://github.com/ossf/alpha-omega/blob/main/SECURITY.md).

