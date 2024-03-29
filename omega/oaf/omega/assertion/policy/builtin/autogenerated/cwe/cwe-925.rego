package openssf.omega.policy.autogenerated.cwe.cwe_925

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_925
# title: "CWE-925: Improper Verification of Intent by Broadcast Receiver"
# methodology: >
#   The Android application uses a Broadcast Receiver that receives an Intent but does not properly verify that the Intent came from an authorized source.
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
        not "cwe-925" in assertion.predicate.content.tags
    }
}