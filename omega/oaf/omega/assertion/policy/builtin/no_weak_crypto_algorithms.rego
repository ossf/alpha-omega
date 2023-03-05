package openssf.omega.policy.no_weak_crypto_algorithms

# Metadata (YAML)
# ---
# name: no_weak_crypto_algorithms
# title: No indicators of weak cryptographic algorithms were found.
# methodology: >
#   This policy is used to ensure that weak cryptographic algorithms are not
#   referenced.
# version: 0.1.0
# last_updated:
#   date: 2023-03-02
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---
import future.keywords.every

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.characteristic"
    input.predicateType == "https://github.com/ossf/alpha-omega/characteristic/0.1.0"
}

pass := true {
    every assertion in input {
        not "cryptography.hashalgorithm.md4" in assertion.predicate.content.characteristics
        not "cryptography.hashalgorithm.md5" in assertion.predicate.content.characteristics
        not "cryptography.hashalgorithm.sha1" in assertion.predicate.content.characteristics
    }
}