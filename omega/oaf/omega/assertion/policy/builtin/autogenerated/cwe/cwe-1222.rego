package openssf.omega.policy.autogenerated.cwe.cwe_1222

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_1222
# title: "CWE-1222: Insufficient Granularity of Address Regions Protected by Register Locks"
# methodology: >
#   The product defines a large address region protected from modification by the same register lock control bit. This results in a conflict between the functional requirement that some addresses need to be writable by software during operation and the security requirement that the system configuration lock bit must be set during the boot process.
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
        not "cwe-1222" in assertion.predicate.content.tags
    }
}