# Update March 2026

This report summarizes the accomplishments made during March 2026 within the OpenJS Ecosystem and Node.js project, spanning major security releases, critical policy changes, release schedule evolution, and community engagement initiatives.

## Node.js

### March 2026 Security Releases

On **Tuesday, March 24, 2026**, the Node.js project published comprehensive security updates across all active release lines (v20.x, v22.x, v24.x, and v25.x), addressing **9 CVEs** ranging from High to Low severity. This release represents one of the most significant security updates in recent Node.js history, addressing critical vulnerabilities in TLS handling, HTTP processing, Permission Model enforcement, and V8 internals.

**Release versions:**
- Node.js v20.20.2
- Node.js v22.22.2
- Node.js v24.14.1
- Node.js v25.8.2

**Dependency updates:**
- undici (6.24.1, 7.24.4) on 22.x, 24.x, 25.x

Work reference: https://nodejs.org/en/blog/vulnerability/march-2026-security-releases

#### High-Severity Vulnerabilities (2 CVEs)

**CVE-2026-21637: Incomplete fix for TLS SNICallback DoS (High)**

A flaw in Node.js TLS error handling allows attackers to crash servers by sending malformed server names. This represents an incomplete fix of a prior vulnerability where similar issues in other TLS callbacks were already addressed.

**CVE-2026-21710: Denial of Service via `__proto__` header (High)**

A flaw in Node.js HTTP request handling allows attackers to crash servers by sending a specially crafted HTTP header named `__proto__`. When applications access certain header properties, the server crashes with an unhandled error.

#### Medium-Severity Vulnerabilities (5 CVEs)

**CVE-2026-21711: Permission Model bypass for Unix Domain Sockets (Medium)**

A flaw in the Node.js Permission Model allows applications to create local network connections even when network access is restricted. Unix Domain Sockets were not properly covered by the network permission checks.

**CVE-2026-21712: URL processing crash with malformed domain names (Medium)**

A flaw in Node.js URL processing causes crashes when handling malformed internationalized domain names with invalid characters.

**CVE-2026-21713: Timing attack in HMAC verification (Medium)**

A flaw in Node.js HMAC verification allows attackers to potentially guess valid signatures by measuring how long verification takes. The comparison method leaks timing information that could be exploited.

**CVE-2026-21714: Memory leak in HTTP/2 servers (Medium)**

A memory leak occurs in Node.js HTTP/2 servers when clients send malformed flow control messages. The server handles the error correctly but fails to clean up allocated memory.

**CVE-2026-21717: Hash collision attack in V8 (Medium)**

A flaw in V8's string handling allows attackers to cause severe performance degradation by sending specially crafted data that triggers hash collisions. This is particularly easy to exploit with JSON data containing numeric strings.

#### Low-Severity Vulnerabilities (2 CVEs)

**CVE-2026-21715: Permission Model bypass for file path resolution (Low)**

A flaw in the Node.js Permission Model allows applications to check if files exist and resolve file paths even when filesystem read access is restricted. One specific filesystem function was missing permission checks.

**CVE-2026-21716: Incomplete fix for file permission bypass (Low)**

An incomplete fix for a previous vulnerability allows applications to modify file permissions and ownership when using promise-based file operations, even when write access is restricted. The callback-based versions were fixed, but the promise versions were missed.

#### Security Release Impact Analysis

This security release demonstrates several important trends:

1. **Permission Model Maturation**: Three CVEs (CVE-2026-21711, CVE-2026-21715, CVE-2026-21716) relate to Permission Model bypasses, indicating both increased scrutiny of this security feature and the ongoing work to ensure comprehensive enforcement across all Node.js APIs.

2. **Incomplete Fix Pattern**: Two CVEs (CVE-2026-21637, CVE-2026-21716) represent incomplete fixes of prior vulnerabilities, highlighting the importance of comprehensive testing and review of security patches across all API surfaces.

3. **AI-Driven Discovery**: The volume and nature of these reports align with the trend discussed in TSC#1826, where AI-powered fuzzing and scanning tools are discovering edge cases and inconsistencies in error handling and permission enforcement.

4. **Cross-Runtime Coordination**: The V8 HashDoS vulnerability (CVE-2026-21717) required coordination with other V8-based runtimes, demonstrating the importance of ecosystem-wide security collaboration.

### Security Bug Bounty Program Paused

On March 2026, the Node.js project announced the **pause of its security bug bounty program** due to the discontinuation of external funding from the Internet Bug Bounty (IBB) program.

**Background:**
Since 2016, the Node.js project participated in the Internet Bug Bounty (IBB) program through HackerOne, offering monetary rewards to security researchers who responsibly disclosed vulnerabilities. The program was a meaningful part of the Node.js security ecosystem.

**Reason for Pause:**
The Internet Bug Bounty (IBB) program, which supported bounty rewards for Node.js through a pooled donation-funded initiative, has been paused. This decision was not made by the Node.js project. As a volunteer-driven open-source project, Node.js does not have an independent budget to sustain a bounty program on its own.

**What This Means:**
- **Security reporting remains unchanged**: The project still accepts and triages vulnerability reports through HackerOne
- **No monetary rewards**: Reports will no longer be eligible for bounty payouts
- **Same commitment to security**: The Node.js Security Team continues to treat security with the highest priority. The disclosure policy, response times, and release process remain the same

**Looking Ahead:**
The project will re-evaluate resuming the bounty program if dedicated funding becomes available again. Organizations that depend on Node.js and are interested in sponsoring a bug bounty program are encouraged to reach out through the OpenJS Foundation.

**Community Impact:**
The Node.js team expressed sincere gratitude to every researcher who has reported vulnerabilities through the bounty program over the years, acknowledging that their contributions have made Node.js safer for millions of users. The project hopes researchers will continue to report security issues even without financial incentives, as responsible disclosure is critical to the health of the open-source ecosystem.

Work reference: https://nodejs.org/en/blog/announcements/discontinuing-security-bug-bounties

### Evolving the Node.js Release Schedule

In March 2026, the Node.js project announced a **major evolution of its release schedule**, representing the most significant change to the release process in 10 years. The new schedule will take effect starting with **Node.js 27 in October 2026**.

#### Why This Change

**Data-Driven Decision:**
The current release schedule is 10 years old, created during the io.js merger as "an educated guess of what enterprises would need." After a decade of data, the project now has clear evidence of how users actually consume Node.js:

- **Odd-numbered releases see minimal adoption**: Most users wait for Long-Term Support (LTS) versions
- **The odd/even distinction confuses newcomers**: Many don't understand the difference
- **Organizations skip odd releases entirely**: Upgrading only to LTS versions is the norm

**Volunteer Sustainability:**
Node.js is maintained primarily by volunteers. While some contributors receive sponsorship, most work (reviewing PRs, handling security issues, cutting releases, backporting fixes) is done by people in their spare time.

**Critical Challenge:** Managing security releases across four or five active release lines has become difficult to sustain. Each additional line increases backporting complexity. By reducing the number of concurrent release lines, the project can focus on better supporting the releases people actually use.

#### What's Changing (Starting October 2026)

**New Release Model:**
- **One major release per year** (April), with LTS promotion in October
- **Every release becomes LTS** - No more odd/even distinction (Node.js 27 will become LTS)
- **Alpha channel** for early testing with semver-major changes allowed
- **Alpha versioning** follows semver prerelease format (e.g., `27.0.0-alpha.1`)
- **Version numbers align with calendar year** of initial Current release: 27.0.0 in 2027, 28.0.0 in 2028
- **Reduced Releasers' burden** through fewer concurrent release lines

**Total Support Window:** 36 months from first Current release to End of Life (EOL)

#### What's NOT Changing

- **Long-Term Support duration** remains similar (30 months)
- **Migration windows preserved**: Overlap between LTS versions remains
- **Quality standards unchanged**: Same testing, same CITGM, same security process
- **Predictable schedule**: April releases, October LTS promotion
- **V8 adoption cycle**: Node.js latest releases will still include a version of V8 that's at most about 6 months old

#### Timeline

**Node.js 26 (Last release under current model):**
Node.js 26 follows the existing schedule. This is the last release line under the current model.

**Node.js 27 (First release under new model):**
Node.js 27 is the first release line under the new schedule, launching in October 2026.

**The Next 10 Years:**
The schedule is not final and may be amended. The project maintains an up-to-date `schedule.json` in the Release repository for the authoritative support timeline.

**Security Sustainability Impact:**
This change directly addresses security sustainability concerns by reducing the number of concurrent release lines that require security backports, allowing the security team to focus resources more effectively.

Work reference: https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule

### Proposal: Moving Security Reports to a Public Workflow

On **February 26, 2026**, Rafael Gonzaga (Node.js Security Lead) opened a controversial but important discussion in the TSC about fundamentally changing how Node.js handles security reports: **moving from a private to a public workflow**.

#### Context and Motivation

**The Problem:**
Over the last six months, the Node.js project has seen a significant increase in both contributions and HackerOne reports. This surge is largely driven by AI: contributors are using LLMs to fuzz and scan the codebase for potential vulnerabilities, and the reports received are remarkably similar, strongly suggesting they originate from the same or similar LLM/tooling.

**Measures Already Taken:**
1. **Raised HackerOne Signal requirement**: Now requires reporters to have a Signal score of 1.0 or higher to submit reports
2. **Expanded Threat Model**: Clarified what is and isn't in scope in SECURITY.md
3. **Automatic closure**: Reports that don't match requirements are automatically closed

**Why These Measures Aren't Enough:**
Despite these improvements, the team is still overwhelmed. Reports that get automatically closed due to insufficient signal are now reaching the OpenJS CNA email and following the escalation path, threatening to overwhelm that team as well.

#### The Proposal

**Key Insight:**
Most reports received are not vulnerabilities according to the threat model, but that doesn't mean they aren't bugs worth fixing. The reports are also highly duplicated, which reveals something important: **anyone with access to a capable LLM can surface the same findings at any time**. These findings are effectively public already.

**Core Argument:**
If a commonly available tool can reproduce findings on demand, treating them as private secrets provides a false sense of security. Additionally, the disclosure policy is set to 90 days, and anyone could find valid vulnerabilities before a security release is even issued.

**Proposed Solution:**
Handle all security reports through a **public workflow**, similar to how Chromium/V8 operates. Benefits include:

1. **Faster fixes**: Most reports aren't vulnerabilities but are bugs that would get fixed faster if visible to the entire contributor community instead of sitting in a private queue
2. **Freed security team capacity**: Focus on dependency vulnerabilities and shipping releases faster (no need to lock CI and follow all 26 steps for non-vulnerabilities)
3. **Sustainable triage**: Reduces the burden of triaging AI-generated noise
4. **Defined embargo process**: Would still maintain a process for the rare cases that warrant an embargo

**Note:** After discussion, it was clarified that Chromium/V8 does not handle security reports fully in public, though the issue tracker allows flipping visibility of bugs easily.

#### Community Discussion

This proposal has sparked significant discussion within the Node.js TSC and security community about:

- **Balancing transparency with responsible disclosure**
- **Managing AI-generated security reports at scale**
- **Sustainability of volunteer-driven security processes**
- **The changing nature of vulnerability discovery in the AI era**

The discussion is ongoing and represents a critical conversation about the future of open-source security practices in an era of AI-powered vulnerability discovery.

Work reference: https://github.com/nodejs/TSC/issues/1826

### Conference Presentation: The State of Node.js Security

Rafael Gonzaga delivered a talk at **Node.js Congress** titled **"The State of Node.js Security"**, providing a comprehensive overview of:

- Current security initiatives and the Permission Model evolution
- Security release processes and automation improvements
- Challenges facing the security team, including the AI-driven report surge
- The new release schedule and its security sustainability benefits
- Future directions for Node.js security

This presentation provided valuable education to the Node.js community and gathered feedback on security priorities and concerns.

## OpenJS Ecosystem

### OpenJS CNA Operations

The OpenJS Foundation CVE Numbering Authority (CNA) continued operations during March 2026, coordinating vulnerability disclosures across the JavaScript ecosystem.

**Note:** Specific CVE assignments for March 2026 will be documented as they are published.

### Security Collab Space Activities

Continued support for OpenJS projects through:
- Security policy reviews and updates
- Incident Response Plan (IRP) development
- Threat model creation and refinement
- Security best practices guidance