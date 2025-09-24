# [Ecosyste.ms](http://Ecosyste.ms) Statement of Work 

# Context

[ecosyste.ms](http://ecosyste.ms) is a set of **free** resources for developers, researchers and policymakers to help identify, secure, and sustain critical digital infrastructure. [ecosyste.ms](http://ecosyste.ms) can be used to understand and reason about open source software production and use, along with a set of tools that can be used to inspect, process, and interpolate between common standards and patterns in the domain. 

Developed in 2022 with \~$200k of financial support from Schmidt Futures and Open Source Collective [ecosyste.ms](http://ecosyste.ms) is the *second* time that creators Andrew Nesbitt and Benjamin Nickolls have built the world’s most comprehensive and accurate picture of open source software production, usage and interdependency, the previous being open source search engine [Libraries.io](http://Libraries.io) (acquired by and sadly abandoned by Tidelift 2017-2024). [ecosyste.ms](http://ecosyste.ms) is a reaction by the creators to their experiences with Libraries.io:

*We set out to build the infrastructure that would enable a developer to build a [Libraries.io](http://Libraries.io), Tidelift, Snyk, or Thanks.dev within a few weeks.*

[ecosyste.ms](http://ecosyste.ms) currently indexes and tracks changes to 11.5m open source packages and the use of those packages across some 260m open source repositories, comprising 22 billion individual dependencies. As a result [ecosyste.ms](http://ecosyste.ms) *knows* which packages are the most critical to society, who maintains them, and how well they’re able to handle the pressures placed upon them. 

Since its release in 2023 [ecosyste.ms](http://ecossyte.ms) has helped build and launch a [new kind of open source security company](https://socket.dev), expanded support for an [established vulnerability product](https://snyk.io), [changed Microsofts approach to funding open source](https://opensource.microsoft.com/blog/2024/06/27/5-things-we-learned-from-sponsoring-a-sampling-of-our-open-source-dependencies/), and helps countless others publishing research on open source software including the Linux Foundation and Chan Zuckerberg Initiative. ecosyste.ms supports grant making programs like [The Sovereign Tech Fund](https://www.sovereign.tech), [Digital Infrastructure Insights Fund](https://infrastructureinsights.fund), and [Open Technology Fund](https://www.opentech.fund). [ecosyste.ms](http://ecosyste.ms) is currently serving 1.2 billion requests a month from 12m unique users, serving 300GB of data and processing 15M jobs each day. 

[ecosyste.ms](http://ecosyste.ms) is currently supported by a small number (read, two) of commercial clients who pay an annual fee (currently $12k each) to remove the default CC-BY-SA licence in favour of a CC0 licence, allowing commercial clients to utilise data without having to contribute their work back to the community. Open Source Collective, who act as the project’s fiscal host, also support the team through the development of free applications and services like the recently launched [Ecosystem Funds](http://funds.ecosyste.ms), and soon-to-be-launched [Ecosystem Dashboards](http://dashboard.ecosyste.ms), which are created to facilitate the distribution and validation of government-scale investments in open source infrastructure or ‘digital public goods’. 

**Development of these applications is due to come to a natural end September 2025\. As a result [ecosyste.ms](http://ecosyste.ms) is projected to  enter a fallow period at that time.** 

# Goals

This statement of work hopes to achieve strategically significant and aligned goals for both [ecosyste.ms](http://ecosyste.ms) and Alpha-Omega. Specifically the development and maintenance of services that enable Alpha-Omega to scale their programs while providing a foundation for [ecosyste.ms](http://ecosyste.ms) to sustain their work now, and for the foreseeable future. 

Broadly the SoW hopes to drive:

* **Adoption**: Expanding awareness and adoption of [ecosyste.ms](http://ecosyste.ms) across open source producing and supporting communities.  
* **Business**: Expanding [ecosyste.ms](http://ecosyste.ms)’ business model to include paid for request prioritisation, corporate deployment of the services inside the organisation, and a new public-private data processing pipeline that enables companies to build atop of and contribute data back to [ecosyste.ms](http://ecosyste.ms).   
* **Community**: Create and support a community of code and data contributors through a plugin-based analysis ‘marketplace’ and improvements to encourage core platform contributors to become future maintainers.   
* **Development**: To refactor the current architecture into a processing ‘pipeline’ supporting abstract analysis informed by and in response to [ecosyste.ms](http://ecosyste.ms)’ event monitoring stream, permitting Alpha Omega and others to contribute analysis and data to the commons or create repositories of data for private use both on and off-site.    
* **Enterprise:** Develop and support an enterprise licensing model, while scoping further ‘public-private cloud’ hosted deployment strategies for efficient use of [ecosyste.ms](http://ecosyste.ms)’ hosted data and event stream while maintaining end user privacy for commercially sensitive users. 

# Projects

The following projects aim to deliver the goals stated above in a piecemeal fashion. Each project has a clear goal, short description of the work to be completed, a budget and timeline. 

The API Policy work is considered a dependency of the primary ‘Data Pipeline’ project. Similarly the ‘Contributor Onboarding’ project is considered a pre-requisite to the ‘Cloud hosting’ project due to the expected support load generated by undocumented configuration and behaviours.

A proposed project plan, incorporating all elements is available at [https://github.com/orgs/ecosyste-ms/projects/10/views/1](https://github.com/orgs/ecosyste-ms/projects/10/views/1) and incorporates these dependencies. 

## 1 API Policy

**Goal:** Business: professional users can pay for enhanced access when developing customer-facing products.   
**What:** Enable essential API auth, limits, licensing, revenue, and metrics to allow per-client policies.

In order to better understand and support users of [ecosyste.ms](http://ecosyste.ms), and to support the corresponding cost of service provision, the team will develop user agent tracking and rate limiting alongside paid API key provisioning for users requiring request prioritisation across all services.

Importantly [ecosyste.ms](http://ecosyste.ms) will continue to offer a free service, capable of supporting experiments and prototypes alongside broader ‘read only’ analysis intended on supporting research and policymaking. In addition we will retain the current licensing model supporting those wishing to build upon the commons at an effectively reduced cost. 

This work will include:

* Building pages for licencing, SLAs (on event feeds)  
* Marketing assets, specific campaigns, spots, etc  
* Outreach to users to discuss usage and billing preferences  
* API Gateway provision, tracking, rate limiting, prioritisation  
* Building a billing service (Stripe and/or OSC)  
* Update CLI to incorporate API key

## 2 Contributor onboarding guidance

**Goal:** Community: new contributors can easily get [Ecosyste.ms](http://Ecosyste.ms) running on their local workstation or in one of the three major clouds.  
**What:** Improved automation and documentation for onboarding of new contributors.

### Narrative

To date [ecosyste.ms](http://ecosyste.ms) has been developed and maintained solely by Andrew Nesbitt, representing a significant risk to both the project and the users of the services provided by [ecosyste.ms](http://ecosyste.ms).

In order to reduce this risk our intent is to bring new, paid contractors onto the project as part of the development of other elements of this proposal. In addition we would like to dedicate time to improving developer experience, contributor onboarding, and to create a pathway to becoming a co-maintainer of [ecosyste.ms](http://ecosyste.ms). This will enable professional users to both self-support and to reduce risk by raising the ‘bus factor’, bringing paid maintainers into the project from enterprise customers and partner organisations. 

This work will include:

* Improvements to frontend for end users (descriptive, usage based)  
* Improving technical documentation (standardized across most, 23 main services plus CLI)  
* Project process docs (Goals, Governance, code standards, team, licensing etc)

## 4 Governance and organizational sustainability plan

**Goal**: Business: [ecossyte.ms](http://ecossyt.ms) has the necessary support to make it to a commercial sustainability as a non-profit organization.   
**What:** Develop a long term plan and first steps towards making [Ecosyste.ms](http://Ecosyste.ms) a durable open source institution

While many of the proposals described here are intended to build a more sustainable future for [ecosyste.ms](http://ecossyste.ms) as (effectively) a non-profit business, we believe the project would also benefit from a more foundation-like governance model, incorporating a paid membership scheme. Such a scheme would support the project during its current growth phase, bridging the gap between deployment of new services and products, and financial sustainability. 

[ecosyste.ms](http://ecosyste.ms) is fiscally hosted and supported by Open Source Collective (OSC), a membership organisation legally identical to the Linux Foundation. OSC’s governance structure allows for both corporate (Sponsor) and project (Collective) members to enjoy specific benefits that are broadly compatible with governing and being a supporting member of an open source project (i.e. holding assets, facilitating payments, offering member benefits). 

Our immediate goal is to explore whether it is practical to govern [ecosyste.ms](http://ecosyste.ms) in a way that is compatible with its existing relationship with OSC, to determine at what point, it would be necessary to form a separate entity with its own formal governance and membership structure, and to implement a governance protocol in line with and alongside a small group of partner organisations. 

This work would involve:

- Developing financial projections based on current and forecasted revenues and costs  
- Developing a governance framework, and establishing ‘bylaws’  
- Recruiting members, a board, and any required committees  
- Documenting and publishing governance framework and necessary outputs (agendas, minutes, etc)  
- Other public engagement activities (blog posts, etc)

