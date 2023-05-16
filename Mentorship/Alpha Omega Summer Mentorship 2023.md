

# Alpha Omega Summer Mentorship 2023

**Term:** June- August

**Number of Mentees:** 4

**Mentors:** Jonathan Leitschu and Yesenia Yser 

**Stipend:** $17,500/ Mentee 

Alpha Omega Summer Mentorship program connects Senior Software Security Engineers for the Alpha-Omega OpenSSF project with newcomers to the open source community, software development, or security researcher assisting. Mentee’s joining this program will receive one on one education and support over a 12 week period. Mentees will be awarded stipends in two installments, the first is to be paid out at six weeks, the second at the completion of the program.

Applications for the Summer Mentorship Program are open as of April 10th, 2023. Mentorship application has closed. Program is expected to start on June 1, 2023.


# Program Details

1. [Security Engineer](#A-O Security Engineer Mentee)
2. [Security Research](#A-O Security Research Mentee)

---


## A-O Security Engineer Mentee


### Relevant Knowledge

* Languages (in order of priority): Python, Python-Django, CSS, HTML, Redis, Postgres
* Interest in Security, Software Development, Vulnerability Management, DevSecOps, and Security Research

# Projects

Below is a list of defined projects to aspire for during the Summer 2023 mentorship program. The phases will be high level as the individual tasks depend on the project assigned and an individual contributor's experience and interest. 

Overall Goal: Establish communication and connection between the Omega Analyzer and the Triage Portal.
1. Create a method to connect the Omega analyzer to the Triage Portal (local dev + prod).
2. Engineer an API endpoint from the Triage Portal so the Omega analyzer can automatically send SARIF files.
3. Implement a Vulnerability workflow process within the Triage Portal to assist with Security Research triaging lifecycle.

# Phases

## All Phases

General items that are relevant at any point

* Attend and participate in relevant OpenSSF working group meetings, including, but not limited to: Vulnerability Disclosures WG & Vulnerabilities Disclosures WG SIG Autofix
* Watch recordings of previous year Black Hat and DEF CON talks for inspiration and continuing education.
* Watch recordings of Linux Foundation training videos on Open Source Software community, best practices, ethics and standard. 
* Enhance the onboarding, how-to, and offboarding documentation for the tooling and the program.
* Provide a weekly status report to their mentors during 1-1 sync and team syncs.
* All documentation, visual representations, and github issues are to be shared in the OpenSSF #alpha-omega channel to promote additional collaboration.
* All demos and recording will go on mentee’s personal youtube or digital portfolio website


## Phase I:  Establish Base Familiarity

This is a high level outline of expected tasks to be completed. This phase will be approximately 6 weeks in time. 


* Research + Onboarding (2 weeks)
    * Become familiar with project tooling
    * Build out tooling in local workstation, Github CodeSpace, or via cloud provider
    * Enhance the onboarding build process and documentation
    * Draft out initial research of the problem, scope, and areas of research
* Design (2-3 weeks)
    * Research the technical details required to solve the problem
    * Document a SW Requirement documentation on the technical design, to include use case, security requirements, and test requirements
    * If applicable, provide a proof of concept or visual demonstration / visualization of solution
    * Provide a status report on a). Problem and the solution; b). What you learned, c). What challenges have you faced?
* Presentation and Alignment ( 1 week)
    * Gather community feedback via channels outside of the Alpha-Omega team
    * Gather feedback from the Alpha-Omega team
    * Provide a 30-min presentation on a). Problem and the solution; b). What you learned?, c). What challenges have you faced?, d). What did you accomplish?


## Phase II: Implement Knowledge

This is a high level outline of expected tasks to be completed. This phase will be approximately 6 weeks in time. The fine grained details of this phase will be relevant and understandable during the Design steps of Phase I. 



* Implementation (3 weeks)
    * Implement the reviewed functionality solution
    * Raise any challenges or blockers, as soon as possible, to mentor
    * Documentation on how-to use and update any documentation on functionality changes
* Testing (2 weeks)
    * Provide test cases based on the SW requirement documents, use cases, and security requirements
    * Provide documentation on test cases; a). What is covered?, b). Areas of test not covered, c). Improvements and future functionality
* Offboarding (1 week)
    * Record demo on the new functionality
    * Documentation on a). Next steps, b). What works, c). What does not work, d). Future challenges, e). Fresh perspective
    * Provide a 30-min presentation on a). Problem and the solution; b). What you learned?, c). What challenges have you faced?, d). What did you accomplish?
    * Respond to a program feedback survey
    * Offboarding call with mentor


## A-O Security Research Mentee

### Relevant Knowledge

* Languages (in order of priority): Java, Python, Kotlin
* Interest in Security and Security Research

# Phases

## All Phases

General items that are relevant at any point

* Attend and participate in relevant OpenSSF working group meetings, including, but not limited to: Vulnerability Disclosures WG & Vulnerabilities Disclosures WG SIG Autofix
* Watch recordings of previous year Black Hat and DEF CON talks for inspiration and continuing education.
* Watch recordings of Linux Foundation training videos on Open Source Software community, best practices, ethics and standard. 
* Enhance the onboarding, how-to, and offboarding documentation for the tooling and the program.
* Provide a weekly status report to their mentors during 1-1 sync and team syncs.
* All documentation, visual representations, and github issues are to be shared in the OpenSSF #alpha-omega channel to promote additional collaboration.
* All demos and recording will go on mentee’s personal youtube or digital portfolio website

## Phase I:  Establish Base Familiarity

SOME of these tasks will be completed
* OpenRewrite
  * Become familiar with OpenRewrite and AST manipulation
  * Write a basic OpenRewrite recipe
  * Become familiar with OpenRewrite’s Control Flow and DataFlow API
* CodeQL
  * Setup CodeQL Development Environment
  * Become familiar with CodeQL’s API including DataFlow and Control Flow
  * Write a simple CodeQL query to find common code patterns
  * Become familiar with CodeQL’’s Control Flow and DataFlow API
* Omega-Moderne Client
  * Become familiar with the codebase
* Documentation
  * Enhance the onboarding build process and documentation
  * Provide a status report on 
    * a). Problem and the solution; 
    * b). What you learned, 
    * c). What challenges have you faced?
  * Gather community feedback via channels outside of the Alpha-Omega team
  * Gather feedback from the Alpha-Omega team
  * Provide a 30-min presentation on 
    * a). Problem and the solution; 
    * b). What you learned?, 
    * c). What challenges have you faced?, 
    * d). What did you accomplish?

## Phase II: Implement Knowledge

SOME of these tasks will be completed
All of these efforts will need to be more actively collaborative between myself and the mentee.

* CodeQL
  * Leverage CodeQL to detect variants of a new or existing vulnerability.
  * Contribute the query to the GitHub Security Lab Bug Bounty program
* OpenRewrite
  * Expand Control Flow and DataFlow to support multi-file analysis
  * Apply DataFlow and ControlFlow to write a recipe to detect and remediate a class of vulnerabilities.
* Vulnerability Reporting
  * Exposure to the vulnerability disclosure process.
  * Report a real security vulnerability to an OSS project.
* Documentation
  * Raise any challenges or blockers, as soon as possible, to mentor
  * Documentation on how-to use and update any documentation on functionality changes
  * Record demo on the new functionality, process, or research
  * Documentation on 
    * a). Next steps, 
    * b). What works, 
    * c). What does not work, 
    * d). Future challenges, 
    * e). Fresh perspective
  * Provide a 30-min presentation on a). Problem and the solution; b). What you learned?, c). What challenges have you faced?, d). What did you accomplish?
  * Respond to a program feedback survey
  * Offboarding call with mentor
