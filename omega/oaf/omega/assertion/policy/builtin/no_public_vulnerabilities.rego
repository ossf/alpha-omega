package openssf.omega.policy.no_public_vulnerabilities

# Metadata (YAML)
# ---
# name: no_public_vulnerabilities
# title: No publicly-known vulnerabilities exist.
# methodology: >
#   This policy is used to determine if a project contains any publicly-known
#   vulnerability.
# version: 0.1.1
# last_updated:
#   date: 2022-12-10
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---

import future.keywords.every

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.security_advisories"
    input.predicateType == "https://github.com/ossf/alpha-omega/security_advisories/0.1.0"
    input.predicate.content
}

pass := true {
    every assertion in input {
        assertion.predicate.content.security_advisories == {}
    }
}