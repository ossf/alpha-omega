package openssf.omega.policy.process.has_a_license

# Metadata (YAML)
# ---
# name: process.has_a_license
# title: Subject has a declared license
# methodology: >
#   This policy is used to determine if a subject has a declared license, such
#   as through a LICENSE or COPYRIGHT file. It uses the OpenSSF scorecard
#   project to determine this.
# version: 0.1.0
# last_updated:
#   date: 2023-03-02
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---
import future.keywords.in

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.security_scorecard"
    input.predicateType == "https://github.com/ossf/alpha-omega/security_scorecard/0.1.0"
}

pass := true {
    some assertion in input
    to_number(assertion.predicate.content.scorecard_data.license) >= 7
}

