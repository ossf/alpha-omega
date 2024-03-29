package openssf.omega.policy.autogenerated.cwe.cwe_207

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_207
# title: "CWE-207: Observable Behavioral Discrepancy With Equivalent Products"
# methodology: >
#   The product operates in an environment in which its existence or specific identity should not be known, but it behaves differently than other products with equivalent functionality, in a way that is observable to an attacker.
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
        not "cwe-207" in assertion.predicate.content.tags
    }
}