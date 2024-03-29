package openssf.omega.policy.autogenerated.cwe.cwe_943

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_943
# title: "CWE-943: Improper Neutralization of Special Elements in Data Query Logic"
# methodology: >
#   The product generates a query intended to access or manipulate data in a data store such as a database, but it does not neutralize or incorrectly neutralizes special elements that can modify the intended logic of the query.
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
        not "cwe-943" in assertion.predicate.content.tags
    }
}