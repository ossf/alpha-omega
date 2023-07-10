# Analyzer

## Objective
- Enhancement to the analyzer to combine the scan results and assertion report into a single file, while providing the additional functionality from sending the file to local or API instance.


## Use Case
1. Support functionality to support uploading the single SARIF report to the Triage Portal API (local, production, or stdout)
1. Support functionality to combine scan results and assertion into a single run and a SARIF report
1. Design requirements for input improvements to support cadence runs and bulk request (i.e, scan 10 oss projects at once)
1. Use the Analyzer to scan pypi open source projects and report status

## Diagram
```mermaid
---
Analyzer Diagram
---

stateDiagram-v2
	direction TB
	
	state AssertFlagCond <<choice>>
	state TriagePushCond <<choice>>
	
	[*] --> Omega_Analyzer: Request bulk packet scan
	Omega_Analyzer --> AssertFlag
    
    AssertFlag --> AssertFlagCond
    
		
	AssertFlagCond --> Assertion_Framework: Yes
	AssertFlagCond --> TriagePush: No
	
	Assertion_Framework --> TriagePush
    TriagePush --> TriagePushCond
	
	TriagePushCond --> Triage_Portal: Yes
	TriagePushCond --> Local_Computer: No

```


## Requirements
- Use Case #1 & #2 should be designed and implemented
### Use Case 1
- [ ] Push 'summary-results.sarif' to the triage-portal
- [ ] Triage Portal credentials should be supported as environment variable (be sure to change the .env template)
- [ ] Triage Portal Credentials should be passed as parameters when running the ./runtools.sh command
- Exception Handling on the following:
  - [ ] Triage Portal isn't available
	- [ ] Perform 3 Retry Attempts, then default to stdout
  - [ ] Triage Portal does not support or issue with the formatting
  - [ ] User hasn't supplied enough information to connect to triage portal
- [ ] Error should be returned to the user via stdout with a standard log message and HTTP error code, if necessary. 
  - If error occurs on the triage portal, then user should get the HTTP code plus error message
- [ ] Should be able to scan all packages (with a Focus on being more or less compatible with JavaScript [npm], Java [maven] and Python [PyPi]) 


### Use Case 2
- [ ] Running assertion on a package should be supported by environment variables
  - [ ] For frequent and/or cadence, support an assertionReport option to always run the assertion report
- [ ] Running assertion on a package should be supported by passing as an parameter when running the ./runtools.sh command
- [ ] The scan and assertion should run at the same time
  - [ ] Assume that each will take time (assertion and scan)
  - [ ] Prevent "timeouts" as best as possible
- [ ] The assertion report should be included in the final 'summary-results.sarif' file
- [ ] The assertion report scheme should have a key-value pair for the triage portal to easily identify the report data required for parsing
  - ex. "assertion-results"={}

### Use Case 3
- TBD

### Use Case 4 - No test cases needed
- [ ] Keep results in Google Drive (until prod triage portal)
- [ ] Top-level stats on Google Drive
- [ ] Scanning 10 pypis a week
  - [ ] Record failures and status of results
  - [x] Record time to scan 
  - [ ] Rxcord summary-results.sarif file size
  - [ ] Record date of scan

## Bug fixes and additional functionalities implemented
- ./runtools.sh argument and options parsing 
  - https://github.com/ossf/alpha-omega/pull/162 

- ./runtools.sh dynamic version resolution
  - https://github.com/ossf/alpha-omega/pull/162 


## Security Requirements
- [ ] Threat: Maniupulation of Binaries / Files
  - [ ] Remediation: Checksum validation
- [ ] Manipulation on package name / version number
  - Package and Version Validation
- :heady_check_mark: Erroneous data mitgiation
  - One [x] package per container


## Acceptance Criteria
- [ ] The Analyzer pushse the final SARIF file to the Triage Portal's Endpoint
- [ ] The Analyzer has multiple methods to pass the credentials to establish a connection to the Triage Portal
  - Environment Variables or as an argument
- [ ] The analyzer should have support for JavaScript [npm], Java [maven], and Python [PyPi]
- [ ] The analyzer has exception handling for the SARIF file upload
- [ ] Txe analyzer is able to create a SARIF file with only the Scan results
- [ ] The analyzer is able to create a SARIF file to include both the scan results and the assertion report
- [ ] The analyzer has been tested with the Omega Top 10k list despite success of the scan.
- [ ] Tested Omega top 10k list has been documented based on its success and failure
- [ ] The anayzer is used every week to scan 10 pypi project from the Omega Top 10k list
- [ ] The results from the scanned pypi projects are recorded to include scan dureation and success
- [ ] Send a checksum from the analyzer side
  - Simple Hashing --> Digital Signatures (GPG / PGP)

## Future Improvements

## Testing
| Test No | Description | Files  | Steps 
| :---- | :---- | :---- | :---- 
| 1 | Analyzer Build Script           |
| 2 | Analyzer Build Script with Flag | 
| 3 | Version Resolution              |
| 4 | Analyzer do assertion           | 
| 5 | Failure on Errorenous Version   |
| 6 | Failure on invalid input format |
| 7 | ....


### 1
| Steps | Linux Steps | Current Directory 
| :----- | :----: | :----
| Clone Alpha-Omega Repository | `git clone git@github.com:ossf/alpha-omega.git` | .
| Change Directory to omega/analyzer | `cd omega/analyzer` | ./alpha-omega/omega/analyzer 
| Build Container (using build script) | `./build.sh` | ./alpha-omega/omega/analyzer
| Run toolshed container using format | `docker run --rm -it --env-file <.env containing the libaries io creds> openssf/omega-toolshed pkg:npm/left-pad@latest` | ./alpha-omega/omega/analyzer

### 2
| Steps | Linux Steps | Current Directory 
| :----- | :----: | :----
| Clone Alpha-Omega Repository | `git clone git@github.com:ossf/alpha-omega.git` | .
| Change Directory to omega/analyzer | `cd omega/analyzer` | ./alpha-omega/omega/analyzer 
| Build Container (using build script with force flag) | `./build.sh -f` | ./alpha-omega/omega/analyzer
| Run toolshed container using format | `docker run --rm -it --env-file <.env containing the libaries io creds> openssf/omega-toolshed pkg:npm/left-pad@latest` | ./alpha-omega/omega/analyzer

### 3
| Steps | Linux Steps | Current Directory 
| :----- | :----: | :----
| Clone Alpha-Omega Repository | `git clone git@github.com:ossf/alpha-omega.git` | .
| Change Directory to omega/analyzer | `cd omega/analyzer` | ./alpha-omega/omega/analyzer 
| Build Container (using build script) | `./build.sh` | ./alpha-omega/omega/analyzer
| Run toolshed container using format | `docker run --rm -it --env-file <.env containing the libaries io creds> openssf/omega-toolshed pkg:npm/left-pad@latest` | ./alpha-omega/omega/analyzer
| Verify that @latest resolves to a version (i.e returns an output directory | --- | ./alpha-omega/omega/analyzer

### 4
| Steps | Linux Steps | Current Directory 
| :----- | :----: | :----
| Clone Alpha-Omega Repository | `git clone git@github.com:ossf/alpha-omega.git` | .
| Change Directory to omega/analyzer | `cd omega/analyzer` | ./alpha-omega/omega/analyzer 
| Build Container (using build script) | `./build.sh` | ./alpha-omega/omega/analyzer
| Run toolshed container using format | `docker run --rm -it --env-file <.env containing the libaries io creds> openssf/omega-toolshed pkg:npm/left-pad@latest` | ./alpha-omega/omega/analyzer
| Verify that @latest resolves to a version (i.e returns an output directory | --- | ./alpha-omega/omega/analyzer
| Verify that assertion results are within the summary-results.sarif file | `find . -name 'summary-results.sarif' -exec grep 'assertion-results' {} \;` | ./alpha-omega/omega/analyzer

- -v .:/opt/export is used to mount to get content from the container to local machine

### 5
| Steps | Linux Steps | Current Directory 
| :----- | :----: | :----
| Clone Alpha-Omega Repository | `git clone git@github.com:ossf/alpha-omega.git` | .
| Change Directory to omega/analyzer | `cd omega/analyzer` | ./alpha-omega/omega/analyzer 
| Build Container (using build script) | `./build.sh` | ./alpha-omega/omega/analyzer
| Run toolshed container using format | `docker run --rm -it --env-file <.env containing the libaries io creds> openssf/omega-toolshed pkg:npm/left-pad@latest` | ./alpha-omega/omega/analyzer
| Verify that container fails (outputs could not find package: Package could not be found, nothing to do) | --- | ./alpha-omega/omega/analyzer
