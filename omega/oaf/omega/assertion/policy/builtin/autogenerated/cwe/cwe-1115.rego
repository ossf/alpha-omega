package openssf.omega.policy.autogenerated.cwe.cwe_1115

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_1115
# title: "CWE-1115: Source Code Element without Standard Prologue"
# methodology: >
#   The source code contains elements such as source files that do not consistently provide a prologue or header that has been standardized for the project.
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
        not "cwe-1115" in assertion.predicate.content.tags
    }
}