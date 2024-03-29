package openssf.omega.policy.autogenerated.cwe.cwe_91

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_91
# title: "CWE-91: XML Injection (aka Blind XPath Injection)"
# methodology: >
#   The product does not properly neutralize special elements that are used in XML, allowing attackers to modify the syntax, content, or commands of the XML before it is processed by an end system.
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
        not "cwe-91" in assertion.predicate.content.tags
    }
}