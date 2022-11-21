package openssf.omega.policy.no_critical_vulnerabilities

# Metadata (YAML)
# ---
# title: No publicly-known critical vulnerabilities exist.
# methodology: >
#   This policy is used to determine if a project contains any publicly-known
#   critical vulnerability. "Critical" is defined by the `openssf.omega.security_advisories`
#   assertion.
# version: 0.1.1
# last_updated:
#   date: 2022-11-18
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---

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