package openssf.omega.policy.autogenerated.cwe.cwe_495

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_495
# title: "CWE-495: Private Data Structure Returned From A Public Method"
# methodology: >
#   The product has a method that is declared public, but returns a reference to a private data structure, which could then be modified in unexpected ways.
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
        not "cwe-495" in assertion.predicate.content.tags
    }
}