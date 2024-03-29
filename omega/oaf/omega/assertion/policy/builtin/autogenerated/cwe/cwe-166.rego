package openssf.omega.policy.autogenerated.cwe.cwe_166

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_166
# title: "CWE-166: Improper Handling of Missing Special Element"
# methodology: >
#   The product receives input from an upstream component, but it does not handle or incorrectly handles when an expected special element is missing.
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
        not "cwe-166" in assertion.predicate.content.tags
    }
}