# Update March 2025

This report summarizes the accomplishments made during March 2025 within the Node.js project, spanning security disclosure practices, automation improvements, release preparations, and policy updates.

## Node.js

### CVEs for End-of-Life (EOL) Versions – MITRE Removal and Next Steps

In early March, the Node.js Security Team was informed that the CVEs previously issued for EOL versions (Node.js v17 and earlier, v19, and v21) were removed by MITRE. The justification cited adherence to existing CVE program rules but acknowledged that the decision does not reflect the CVE Program’s long-term stance.

To address the implications, the Node.js team:
- Participated in the OpenSSF Vulnerability Disclosure Working Group to express the need for CVEs to include EOL versions.
- Proposed a mitigation plan that includes:
  - [x] Opening a tracking issue to coordinate next steps ([nodejs/security-wg#1443](https://github.com/nodejs/security-wg/issues/1443)).
  - [x] Publishing a blog post to explain the situation and guidance to users: [Updates on CVE for End-of-Life Versions](https://nodejs.org/en/blog/vulnerability/updates-cve-for-end-of-life).
  - [ ] Updating the CVEs to explicitly list EOL versions as affected.
  - [ ] Updating the blog post after these changes are applied.

The goal remains to ensure clear, accurate communication of risks associated with unsupported versions, particularly given their continued high usage in the ecosystem.

### Improving Visibility of Security Patches

A new discussion was initiated to increase visibility into the security patches shipped in Node.js. The TSC is evaluating ways to make this information more accessible to downstream users and security teams. One proposed approach is to improve the discoverability and clarity of security-related commits and changelogs.

- Issue discussion: https://github.com/nodejs/TSC/issues/1687
- Proposed policy update: https://github.com/nodejs/node/pull/57309

### Automation Enhancements in Security Releases

To further reduce manual effort and increase reliability in the security release workflow, the following improvements were made:
- Fixed automation logic for commit and changelog generation:
  - https://github.com/nodejs/node-core-utils/pull/910
  - https://github.com/nodejs-private/security-release/issues/48

These changes ensure changelogs and commit messages are accurate and consistent across security releases.

### Node.js 24 Preparation

Work has started on the next major release of Node.js (v24), which includes branch preparation, release candidate coordination, and changelog generation:
- https://github.com/nodejs/Release/issues/1081

The release is currently targeted for April 2025.

### Node.js Threat Model Update

The Node.js Threat Model was updated to include explicit language about the risks of arbitrary code execution and the expected capabilities of potential attackers:
- https://github.com/nodejs/node/pull/57426

This clarification helps align security expectations across contributors and maintainers.

### Documentation and Policy Updates

Several updates were made to internal and contributor-facing documentation:
- A note was added about syncing private branches used during security releases: https://github.com/nodejs/node/pull/57404
- The security report policy was updated to clarify alignment with the project’s Code of Conduct and responsible disclosure expectations: https://github.com/nodejs/node/pull/57607

### External Engagement

- The team reviewed and discussed the [OpenSSF npm Best Practices Guide](https://docs.google.com/document/d/1fek97rVlUXO41pQUOkW6aZE2Jwx9m1PlvNSnEVtmU0M/edit) as part of the Secure Release Guide initiative.
- Participated in GitHub’s Secure Open Source Course to align Node.js practices with broader ecosystem security standards.

## OpenJS Security Collab Space

### OpenJS CVE Numbering Authority (CNA)

A CVE program-wide pause on accepting new CNAs has been lifted and the OpenJS Security Collab Space met with [Red Hat to be our Root CNA](https://access.redhat.com/articles/red_hat_cve_program).

- The OpenJS CNA is scheduled to be announced and launch on Tuesday 15 April.

### OpenJS Project npm Continuity Policy

The OpenJS [Cross Project Council](https://github.com/openjs-foundation/cross-project-council/issues/1355) is seeking to implement a continuity policy for npm to ensure hosted project packages remain accessible and managable.

- Drafted and incorporated feedback for proposed [npm Continuity Policy text](https://docs.google.com/document/d/1iaNEO8pYjkeog_rqASWaa9rjn_8kHpCWDXa7qy2G418/edit?tab=t.j66rkgmy0xcr).
- Proposed OpenJS npm owner account management security plan.

### OpenJS Secure Releases Guide v2 Update

- Continued to build Security Collab Space consensus about a potential outline for the planned update to the Secure Releases Guide in H2 by forking/updating the [OpenSSF npm Best Practices Guide](https://github.com/ossf/package-manager-best-practices/blob/main/published/npm.md).
- Authored [summary of npm's permissions structures](https://docs.google.com/document/d/1iaNEO8pYjkeog_rqASWaa9rjn_8kHpCWDXa7qy2G418/edit?tab=t.0) to prototype new content for Secure Releases guide. Also used inform npm continuity policy and security compliance guide update.

### OpenJS Security Compliance Guide v1.1 Update

[v1.1 of the OpenJS Security Compliance Guide](https://docs.google.com/spreadsheets/d/1GwIsAudAn89xv9DAbr1HUaY4KEVBsYfg--_1cW0uIB0/edit?pli=1&gid=924266915#gid=924266915) incorporated new guidelines for npm and several other updates based on feedback and IRL use observations:
- Rephrased some entries for clarity
- Moved two dependency-related entries to from Expected to Recommended
- Reorganized content and added Qualifier column to improve interview flow 
