package openssf.omega.policy.autogenerated.cwe.cwe_1335

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_1335
# title: "CWE-1335: Incorrect Bitwise Shift of Integer"
# methodology: >
#   An integer value is specified to be shifted by a negative amount or an amount greater than or equal to the number of bits contained in the value causing an unexpected or indeterminate result.
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
        not "cwe-1335" in assertion.predicate.content.tags
    }
}