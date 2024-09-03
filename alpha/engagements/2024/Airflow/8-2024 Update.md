# Update 2024-08

## Project progress

The project started 1.08.2024. During the first month, the following
steps have been taken and accomplished:

* [Project Meta-Health Audit Concepts](https://docs.google.com/document/d/1LYiINcybGzdqrhlBFXuWlh3zSmGSL4J6DNSHHg4dbg8/edit#heading=h.t6q6qdb2lxpt) - document was
  prepared where idea of “meta health” of projects was explored and iterated on - set of scorecards and signals for projects that would provide a general overview of project’s “security health” and indicate the need of prioritizing direct interaction with the project
* Iterations of semi-automated (and later automated) reports of All 700+ airflow dependencies “meta health scorecard”
  have been produced:
  * [Initial export of dependencies Airflow 2.9.3 - 4.08.2024](https://docs.google.com/spreadsheets/d/1qNSfp6HxVrhU3l9I-LOlmnSedWqsIAe75RxT37kZpGw/edit?usp=drive_link)
  * [Airflow Dependencies export: 2.10  21.08.2024](https://docs.google.com/spreadsheets/d/15Os3hQnKo9GXCuCaSOx90CsizwmIFnAfMcat8Vt1Wpo/edit?usp=drive_link)
  * [Airflow Dependencies export: 2.10  31.08.2024](https://docs.google.com/spreadsheets/d/1IT8PMEhtvhwSgH9ksXl97F-NJKez0wR7gTgP6NiMcJk/edit?usp=drive_link)
    accompanied with [Airflow Dependencies meta-data ](https://docs.google.com/spreadsheets/d/1Hg6_B_irfnqNltnu1OUmt7Ph-K6x-DTWF7GZ5t-G0iI/edit?gid=0#gid=0)
    keeping the data that allows to fully automate future reports and iterations
  * Current report provides automated retrieval and classification of ~ 50% of Airflow
    dependencies - the goal of the project is to improve that rate over time.

The report has been used to identify concrete actions that might be taken when
directly contacting projects (documented in the report itself) and identify
first 16 dependencies that Airflow maintainers should directly contact
and propose improvement actions.

Airflow PMC and security team have been involved to review and provide
feedback to the list of recommended dependencies/actions.

## Recommended actions:

|                   | Add Security Policy to the repository | Follow up with vulnerabilities | Propose Trusted Publishing | Follow up with dangerous workflow | Propose mandatory code review |
|-------------------|:-------------------------------------:|:------------------------------:|:--------------------------:|:---------------------------------:|:-----------------------------:|
| argcomplete       |                                       |                                | Yes                        |                                   | Yes                           |
| asgiref           | Yes                                   |                                | Yes                        |                                   |                               |
| colorlog          | Yes                                   |                                |                            |                                   | Yes                           |
| cron-descriptor   | Yes                                   |                                | Yes                        |                                   | Yes                           |
| croniter          | Yes                                   |                                | Yes                        |                                   | Yes                           |
| deprecated        | Yes                                   |                                | Yes                        |                                   | Yes                           |
| dill              |                                       |                                | Yes                        | Yes                               | Yes                           |
| flask-caching     |                                       |                                | Yes                        |                                   | Yes                           |
| jmespath          | Yes                                   |                                | Yes                        |                                   | Yes                           |
| lazy-object-proxy |                                       | Yes                            | Yes                        |                                   | Yes                           |
| psutil            |                                       |                                | Yes                        |                                   | Yes                           |
| python-nvd3       | Yes                                   | Yes                            | Yes                        |                                   | Yes                           |
| setproctitle      | Yes                                   |                                | Yes                        |                                   | Yes                           |
| tenacity          | Yes                                   |                                | Yes                        |                                   |                               |
| unicodecsv        | Yes                                   |                                | Yes                        | Yes                               | Yes                           |
| universal-pathlib | Yes                                   |                                |                            |                                   | Yes                           |

## Open Refactory bug analysis

Review and follow-ups with [Open Refactory](https://www.openrefactory.com/) has been done. They scanned all
700+ dependencies for possible security bugs and came up with
this [report](https://docs.google.com/spreadsheets/d/1ssQM1HEDVGyogBHG6xLXkpDdtTOprKfI8G0IXIvWeuk/edit?gid=0#gid=0):

* 16 Bugs Reported
* 4 High, 5 Medium, 7 Low severity
  * Weak Cryptography Issues - E.g., Using AES in CBC chaining mode instead of GCM
* Being reported using Private Vulnerability Reporting (PVR)

## Follow up on the issues reported

Follow up to those issues reported with “Apache Airflow maintainer hat”
on had already provided some interesting feedback and reactions.
A number of those issues reported are already addressed or are being addressed.

## "Security United" Keynote at Airflow Summit 2024

Presentation for [Airflow Summit 2024](https://airflowsummit.org/) Keynote “Security United” has been prepared
[Security United: collaborative effort on securing Airflow ecosystem with Alpha-Omega, PSF & ASF](https://docs.google.com/presentation/d/1Da3PsFRRL1PjSkq_Vn09V5fiyJKcbH3Ll5do4wXqG5M/edit#slide=id.p)
and is scheduled to be presented on 10th of September in San Francisco - with the goal of officially announcing the project and spreading awareness of importance of Supply Chain Security
