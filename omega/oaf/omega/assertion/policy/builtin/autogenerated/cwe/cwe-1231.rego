package openssf.omega.policy.autogenerated.cwe.cwe_1231

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_1231
# title: "CWE-1231: Improper Prevention of Lock Bit Modification"
# methodology: >
#   The product uses a trusted lock bit for restricting access to registers, address regions, or other resources, but the product does not prevent the value of the lock bit from being modified after it has been set.
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
        not "cwe-1231" in assertion.predicate.content.tags
    }
}