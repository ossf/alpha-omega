package openssf.omega.policy.autogenerated.cwe.cwe_1257

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_1257
# title: "CWE-1257: Improper Access Control Applied to Mirrored or Aliased Memory Regions"
# methodology: >
#   Aliased or mirrored memory regions in hardware designs may have inconsistent read/write permissions enforced by the hardware. A possible result is that an untrusted agent is blocked from accessing a memory region but is not blocked from accessing the corresponding aliased memory region.
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
        not "cwe-1257" in assertion.predicate.content.tags
    }
}