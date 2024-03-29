package openssf.omega.policy.autogenerated.cwe.cwe_1389

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_1389
# title: "CWE-1389: Incorrect Parsing of Numbers with Different Radices"
# methodology: >
#   The product parses numeric input assuming base 10 (decimal) values, but it does not account for inputs that use a different base number (radix).
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
        not "cwe-1389" in assertion.predicate.content.tags
    }
}