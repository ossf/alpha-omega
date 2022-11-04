package openssf.omega.policy.no_critical_vulnerabilities

# VERSION 0.1.0
# LAST UPDATED 2022-11-03 Michael Scovetta

default pass = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicateGenerator.name == "openssf.omega.security_advisories[deps.dev]"
    input.predicateType == "https://github.com/ossf/alpha-omega/v0.1"
}

pass := true {
    input.predicate.security_advisories
    input.predicate.security_advisories.critical == 0
}