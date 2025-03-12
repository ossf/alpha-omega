# Update December Feb 2025

This report summarizes the accomplishments made during December 2024 and January 2025 within the Node.js project, spanning security initiatives, automation, community engagements, and release processes.

## Node.js

### Initial evaluation of Node.js project against Security Compliance Guide

The Node.js team has also initiated the evaluation of the OpenJS Security Compliance Checker (#1440). This compliance checker will help assess whether the Node.js project and its associated packages adhere to recommended security best practices. The evaluation will categorize compliance status using the following legend:

✅ Applicable and Applied
🟡 Non-Applicable
❌ Applicable and Not Applied
[] Non-verified yet

The assessment covers various aspects of security, including user authentication, account permissions, service authentication, GitHub workflows, vulnerability management, coordinated vulnerability disclosure, code quality, code review, source control, and dependencies. The findings will guide improvements in security practices within the Node.js ecosystem.

Reference: https://github.com/nodejs/security-wg/issues/1440

### CVE to End-of-Life lines

On January 21, 2025, Node.js released security patches for four active release lines and issued CVEs for End-of-Life (EOL) versions: CVE-2025-23087 for Node.js v17 and prior (including v0.x), CVE-2025-23088 for Node.js v19, and CVE-2025-23089 for Node.js v21. This decision has led to discussions within the community.

The Node.js project does not review or include EOL versions in security evaluations due to resource constraints. With more than 20 EOL releases, each having distinct dependencies and build methods, assessments are impractical, and the focus remains on actively supported versions.

Security scanners rely on CVEs to flag vulnerabilities in production environments. If an EOL version is not listed as affected, users might wrongly assume it is secure. The Node.js Technical Steering Committee (TSC) has raised concerns over the continued high usage of EOL versions, such as Node.js v16, which still receives 11 million downloads per month. Issuing CVEs serves as a clear warning that outdated releases likely contain security risks.

The CVEs have been updated with an "Unsupported when assigned" status to reflect their EOL nature, a "Disputed" status indicating they do not reference a specific vulnerability, and a note explaining that using the CVE List for unsupported products is an experimental approach under review.

However, MITRE has requested HackerOne to reject these CVEs, prompting the Node.js team to evaluate the best response while ensuring proper security risk communication. The Node.js team will continue discussions with MITRE and the CVE Program, considering alternative ways to notify organizations about the risks associated with EOL versions. The objective remains to maintain transparency and security awareness for users relying on outdated Node.js versions.

The Node.js team has been discussing it with the security team, TSC and participating in working groups as OpenSSF Security Vulnerability Disclosure WG.

Reference: https://github.com/nodejs/security-wg/issues/1401

### Automation of Security Vulnerability Database

One step more closer to a fully automated security release process. This time, the Node.js team automated the vulnerability PR creation () and included it
as part of the official process https://github.com/nodejs/node/pull/56907.

The Node.js team has taken another step toward a fully automated security release process. This time, the team has automated the creation of vulnerability pull requests, streamlining the reporting and patching workflow. The recent implementation of this automation can be seen in nodejs/security-wg#1437, further reducing manual intervention in the security disclosure pipeline.

### Q1'25 Security Compliance Guide v1.1 Improvements

* Continued work iterate to [v1.1 of the Compliance Guide](https://docs.google.com/spreadsheets/d/1xOWeLCutk5qIRJpfJZ6vsjX1M2DVsJlB5DgDOgygbaE/edit?gid=304502805#gid=304502805):
- Added more guidelines for npm; exploring including other package managers
- Deprecated Priority Group organization
- Separated out items more clearly identify which items apply for different maintainer group sizes
- Updated phrasing of a number of entries for clarity

### H1'25 Secure Release Guide Update

* Kicked off initial discussions and alignment regarding our approach for the new secure release guide. We are [evaluating OpenSSF's npm Best Practices](https://docs.google.com/document/d/1fek97rVlUXO41pQUOkW6aZE2Jwx9m1PlvNSnEVtmU0M/edit?tab=t.0#heading=h.xla7di9m1yob) as a foundational place to work from.

### OpenJS CVE Numbering Authority (CNA) Launch

* Held 6 virtual townhalls for OpenJS maintainers to review the CNA's launch and operations plans, answer questions, and hear requests and feedback.
* RedHat's CNA announced the day before our meeting with them that they are pausing onboarding of new CNAs without an estimated date. We've reached out to MITRE to move the CNA process along.
* Built new OpenJS Security landing page that goes beyond the original CNA website to include resources for project maintainers and consumers.
