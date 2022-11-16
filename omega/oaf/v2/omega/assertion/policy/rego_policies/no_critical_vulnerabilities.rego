package openssf.omega.policy.no_critical_vulnerabilities

# VERSION 0.1.0
# LAST UPDATED 2022-11-03 Michael Scovetta

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.security_advisories"
    input.predicateType == "https://github.com/ossf/alpha-omega/v0.1"
    input.predicate.content.security_advisories
}

pass := true {
    input.predicate.content.security_advisories.critical == 0
} {
    not(input.predicate.content.security_advisories.critical)
}