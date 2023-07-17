package openssf.omega.policy.autogenerated.cwe.cwe_105

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_105
# title: "CWE-105: Struts: Form Field Without Validator"
# methodology: >
#   The product has a form field that is not validated by a corresponding validation form, which can introduce other weaknesses related to insufficient input validation.
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
        not "cwe-105" in assertion.predicate.content.tags
    }
}