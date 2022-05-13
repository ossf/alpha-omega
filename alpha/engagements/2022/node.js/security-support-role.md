## Security Support Role

This document was created after a meeting between Rafael Gonzaga (@rafaelgss) and Michael Dawson (@mhdawson) organized
to align expectations from OpenJS Foundation and Nearform.

The following list is sorted by priority of what OpenJS wants from the partnership. 

### 1) Fix security issues

This responsibility includes

* Analyze and solve reports in HackerOne.
* Triage Node.js issues
* Fixing security vulnerabilities. e.g: HTTP2 Memory Leak.

Requirements
* HackerOne Access – _status: done_

### 2) Dependency analysis/tracking/updates/supply chain

Auditing of dependencies, on all security announcement lists, and automating updates where possible.
Evaluate dependencies in terms of supply chain, components required to rebuild, etc.

Priorities are:

* OpenSSL
* npm

#### 2.1) OpenSSL updates

Currently, OpenSSL updates require a considerable amount of time and work.
For security reasons, OpenSSL versions need to be updated soon as possible in Node.js,
and volunteers are required to perform this work. However, Open-Source projects couldn’t set a deadline for volunteers,
after all, they are volunteers.

The idea is to be in charge of those updates.

Material:

* [Maintaining OpenSSL – Node.js Docs](https://github.com/nodejs/node/blob/master/doc/contributing/maintaining-openssl.md)
* [OpenSSL update instructions – Github Issue](https://github.com/nodejs/node/issues/42395)

### 3) Incoming Triage (HackerOne)

This responsibility includes

* Help triage team with potential security issues
  * Some issues require considerable time to identify if it’s a security vulnerability or not

Requirements

* Onboarded in triage team – _status: in progress_

### 4) Security Releases

Material:

* [OpenJS Security Releases](https://mta.openssl.org/pipermail/openssl-announce/2022-April/000220.html)
* [Adding new releaser – Node.js Docs](https://github.com/nodejs/Release/blob/main/GOVERNANCE.md#adding-new-releasers)
* [Releasing – Node.js Docs](https://github.com/nodejs/node/blob/master/doc/contributing/releases.md)

Requirements

* Onboarded as a Node.js Releaser – _status: in progress_

### 5) Interlocks/Reporting

* Monthly Alpha-Omega public meeting
* [Report form](https://docs.google.com/forms/d/1_nbGPLs3EmioGGs4JjeJJ1_uD-ob8c7eLF5_HarZv8M/viewform?edit_requested=true) monthly

### 6) Improving security processes

This responsibility includes

* Document security best practices
* Define the Threat Model

Material:

* [OpenJSSF Best Practices OS Developers](https://github.com/ossf/wg-best-practices-os-developers)

### 7) Node.js Security Working Group

Revive the Node.js security working group, grow membership, and use it to pull other collaborators into the process
improvement work as much as possible

Material:

* [Reactivating Security WG Meeting - Github Issue](https://github.com/nodejs/security-wg/issues/793)

### 8) Security features

This responsibility is intended to create security features for the Node.js Core.

Example:

* Permission System (It’s already under discussion by Security WG)
* Create a real Sandbox environment
* Build tooling to make policies easier to use

Material:

* [Permission System](https://github.com/nodejs/security-wg/issues/791)

### 9) Security Collaboration Spaces  (Priority will change as they ramp up)

A neutral forum to discuss & ideate across the Node.js ecosystem improving CVE reporting and resolution workflows;
Minimizing the burden on maintainers and noise for consumers

This initiative started and stalled. Sounds feasible to use some time to push it forward.

Material:

* [OpenJS - Package Vulnerability Management & Reporting Collaboration Space](https://github.com/openjs-foundation/pkg-vuln-collab-space)
