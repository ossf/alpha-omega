package openssf.omega.policy.no_cryptographic_implementations

# Metadata (YAML)
# ---
# name: no_cryptographic_implementations
# title: No indicators of cryptographic implementations were found.
# methodology: >
#   This policy is used to ensure that cryptographic algorithms are not
#   implemented.
# version: 0.1.0
# last_updated:
#   date: 2023-03-04
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---
import future.keywords.every

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.cryptoimplementation"
    input.predicateType == "https://github.com/ossf/alpha-omega/cryptoimplementation/0.1.0"
}

pass := true {
    every assertion in input {
        count(assertion.predicate.content.tags) == 0
    }
}