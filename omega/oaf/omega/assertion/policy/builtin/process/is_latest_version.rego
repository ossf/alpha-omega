package openssf.omega.policy.process.is_latest_version

# Metadata (YAML)
# ---
# name: process.is_latest_version
# title: Subject reflects the latest version available.
# methodology: >
#   This policy is used to determine if a subject is the latest version available,
#   so if the subject is version 1.1 and version 1.2 was available, then this policy
#   shoud evaluate to false. It uses the openssf.omega.metadata assertion.
# version: 0.1.1
# last_updated:
#   date: 2022-12-10
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---
import future.keywords.in

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.metadata"
    input.predicateType == "https://github.com/ossf/alpha-omega/metadata/0.1.0"
}

pass := true {
    some assertion in input
    assertion.predicate.content.metadata.is_latest_version == true
}

