package openssf.omega.policy.autogenerated.cwe.cwe_198

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_198
# title: "CWE-198: Use of Incorrect Byte Ordering"
# methodology: >
#   The product receives input from an upstream component, but it does not account for byte ordering (e.g. big-endian and little-endian) when processing the input, causing an incorrect number or value to be used.
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
        not "cwe-198" in assertion.predicate.content.tags
    }
}