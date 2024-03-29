package openssf.omega.policy.autogenerated.cwe.cwe_766

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_766
# title: "CWE-766: Critical Data Element Declared Public"
# methodology: >
#   The product declares a critical variable, field, or member to be public when intended security policy requires it to be private.
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
        not "cwe-766" in assertion.predicate.content.tags
    }
}