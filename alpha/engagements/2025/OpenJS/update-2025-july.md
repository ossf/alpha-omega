# Update July 2025

This report summarizes the accomplishments made during July 2025 within the Node.js project, focusing on security enhancements, permission model improvements, threat model refinements, and community initiatives within the JavaScript ecosystem.

## Node.js

### Permission Model Improvements

Significant enhancements were made to the Node.js Permission Model:

* Enhanced Permission Model Debugging:
  * [https://github.com/nodejs/node/pull/58898](https://github.com/nodejs/node/pull/58898)
  * Improved debugging capabilities when using the `NODE_DEBUG_NATIVE=PERMISSION_MODEL` flag, helping developers better understand permission-related issues

* Process Permission Model Updates:
  * [https://github.com/nodejs/node/pull/58853](https://github.com/nodejs/node/pull/58853)
  * Enhanced the process permission model to provide better security controls and more intuitive developer experience

* Permission Model Edge Case Handling:
  * [https://github.com/nodejs/node/pull/58928](https://github.com/nodejs/node/pull/58928)
  * Fixed edge cases in permission model implementation to ensure consistent behavior across different usage scenarios

### Node.js Security Release

The Node.js project published security releases for all active release lines in July:
* [https://nodejs.org/en/blog/vulnerability/july-2025-security-releases](https://nodejs.org/en/blog/vulnerability/july-2025-security-releases)

Two high severity vulnerabilities were addressed:

#### Windows Device Names Bypass Path Traversal Protection (CVE-2025-27210)

* An incomplete fix was identified for CVE-2025-23084 in Node.js, specifically affecting Windows device names like CON, PRN, and AUX
* This vulnerability could allow attackers to bypass path traversal protections in `path.normalize()`
* Affects all users in active release lines: 20.x, 22.x, 24.x
* Fixed in Node.js v20.19.4, v22.17.1, and v24.4.1

#### HashDoS in V8 (CVE-2025-27209)

* The V8 release used in Node.js v24.0.0 introduced a change to string hash computation using rapidhash
* This implementation re-introduced the HashDoS vulnerability, allowing attackers who can control strings to generate hash collisions
* While the V8 team did not classify this as a security vulnerability, the Node.js project deemed it one due to its potential impact
* This work was coordinated with the Deno team to ensure consistent handling across JavaScript runtimes
* Affects Node.js v24.x users
* Fixed in Node.js v24.4.1

### Improvements to Automation of Security Releases

Multiple improvements were made to the security release tooling:

* Enhanced CVE Request Automation:
  * [https://github.com/nodejs/node-core-utils/pull/956](https://github.com/nodejs/node-core-utils/pull/956)
  * Added patched versions information when requesting CVEs, streamlining the security release process

* Improved Security Release Tooling:
  * [https://github.com/nodejs/node-core-utils/pull/954](https://github.com/nodejs/node-core-utils/pull/954)
  * Enhanced core utilities to better support security release workflows and reduce manual steps

* Security Release Template Updates:
  * [https://github.com/nodejs/node-core-utils/pull/957](https://github.com/nodejs/node-core-utils/pull/957)
  * Improved templates for security release communications to ensure clarity and consistency

### Improvements to Node.js Threat Model

Ongoing work to refine and clarify the Node.js Threat Model continued:

* Path Module Security Documentation:
  * [https://github.com/nodejs/node/pull/59262](https://github.com/nodejs/node/pull/59262)
  * Added clarification for `path.join` and `path.normalize` to establish consistent guidelines for handling path-related security issues

* Threat Model Expansion:
  * [https://github.com/nodejs/node/pull/58917](https://github.com/nodejs/node/pull/58917)
  * Enhanced the threat model documentation to cover additional attack vectors and scenarios, strengthening Node.js security posture

### Security Reports Evaluation

The Node.js HackerOne program remained active, with 7 security reports evaluated during July. These evaluations ensure potential vulnerabilities are properly assessed and addressed in a timely manner, maintaining the security integrity of the Node.js runtime.

## JS Ecosystem

### Security Communication Channels

* Security Help Channel Creation:
  * [https://github.com/openjs-foundation/security-collab-space/issues/284](https://github.com/openjs-foundation/security-collab-space/issues/284)
  * A new `security-help` channel was established to provide assistance to maintainers dealing with security issues, fostering better collaboration across the JavaScript ecosystem

### Project Evaluations

* OpenJS Command Center:
  * [https://github.com/UlisesGascon/openjs-command-center](https://github.com/UlisesGascon/openjs-command-center)
  * Alpha Omega conducted evaluations of OpenJS projects, assessing security posture and identifying opportunities for improvement across the foundation's projects

## Ongoing Work

### Release Schedule Improvements

* New Node.js Release Schedule Discussion:
  * [https://github.com/nodejs/Release/issues/953](https://github.com/nodejs/Release/issues/953)
  * Ongoing discussion regarding potential changes to the Node.js release schedule to better align with community needs and security considerations

### Documentation Enhancements

* Dedicated EOL Page Development:
  * [https://github.com/nodejs/nodejs.org/pull/7990](https://github.com/nodejs/nodejs.org/pull/7990)
  * Work continues on creating a dedicated End-of-Life (EOL) page for the Node.js website to clearly communicate support timelines and help users maintain secure deployments

### Expressjs Bug Bounty

* The team is consolidating a policy ([ref](https://github.com/expressjs/security-wg/pull/90)) to create a public program in the YesWeHack platform.

### Secure Releases Guide (v2.0)

* The team will land soon the Secure Releases Guide v2.0 in the [The Security Collab Space documentation](https://github.com/openjs-foundation/security-collab-space/pull/283)

### Extend Security Best Practices in opensource.guides

* We include additional information about Licenses, reporting, threat models and Incident Responses Plans (IRP) based on our experience implementing these recommendations in the OpenJS Projects. [Details](https://github.com/github/opensource.guide/pull/3465)
