package openssf.omega.policy.autogenerated.cwe.cwe_433

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_433
# title: "CWE-433: Unparsed Raw Web Content Delivery"
# methodology: >
#   The product stores raw content or supporting code under the web document root with an extension that is not specifically handled by the server.
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
        not "cwe-433" in assertion.predicate.content.tags
    }
}