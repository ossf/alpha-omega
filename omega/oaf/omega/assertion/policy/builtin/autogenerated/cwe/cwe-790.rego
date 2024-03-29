package openssf.omega.policy.autogenerated.cwe.cwe_790

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_790
# title: "CWE-790: Improper Filtering of Special Elements"
# methodology: >
#   The product receives data from an upstream component, but does not filter or incorrectly filters special elements before sending it to a downstream component.
# version: 0.1.0
# last_updated:
#   date: 2023-05-25
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---

import future.keywords.every
import future.keywords.in

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.security_tool_finding"
    input.predicateType == "https://github.com/ossf/alpha-omega/security_tool_finding/0.1.0"
    input.predicate.content.tags
}

pass := true {
    every assertion in input {
        not "cwe-790" in assertion.predicate.content.tags
    }
}