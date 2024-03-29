package openssf.omega.policy.autogenerated.cwe.cwe_81

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_81
# title: "CWE-81: Improper Neutralization of Script in an Error Message Web Page"
# methodology: >
#   The product receives input from an upstream component, but it does not neutralize or incorrectly neutralizes special characters that could be interpreted as web-scripting elements when they are sent to an error page.
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
        not "cwe-81" in assertion.predicate.content.tags
    }
}