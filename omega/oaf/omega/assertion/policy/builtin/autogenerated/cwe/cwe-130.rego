package openssf.omega.policy.autogenerated.cwe.cwe_130

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_130
# title: "CWE-130: Improper Handling of Length Parameter Inconsistency"
# methodology: >
#   The product parses a formatted message or structure, but it does not handle or incorrectly handles a length field that is inconsistent with the actual length of the associated data.
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
        not "cwe-130" in assertion.predicate.content.tags
    }
}