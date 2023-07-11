package openssf.omega.policy.process.not_deprecated

# Metadata (YAML)
# ---
# name: process.not_deprecated
# title: Subject is not marked as deprecated.
# methodology: >
#   This policy is used to validate that the project is not marked as
#   deprecated, based on the openssf.omega.metadata assertion.
# version: 0.1.1
# last_updated:
#   date: 2022-12-10
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---
import future.keywords.every

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.metadata"
    input.predicateType == "https://github.com/ossf/alpha-omega/metadata/0.1.0"
}

pass := true {
    every assertion in input {
        assertion.predicate.content.metadata.latest_version_deprecated == false
    }
}
