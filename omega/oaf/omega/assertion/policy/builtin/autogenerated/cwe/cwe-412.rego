package openssf.omega.policy.autogenerated.cwe.cwe_412

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_412
# title: "CWE-412: Unrestricted Externally Accessible Lock"
# methodology: >
#   The product properly checks for the existence of a lock, but the lock can be externally controlled or influenced by an actor that is outside of the intended sphere of control.
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
        not "cwe-412" in assertion.predicate.content.tags
    }
}