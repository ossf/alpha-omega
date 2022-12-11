package openssf.omega.policy.process.actively_maintained

# Metadata (YAML)
# ---
# name: process.actively_maintained
# title: Subject is actively maintained
# methodology: >
#   This policy is used to determine if a project is being actively maintained,
#   based on the scorecard "maintained" score.
# version: 0.1.0
# last_updated:
#   date: 2022-12-16
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
    to_number(assertion.predicate.content.scorecard_data.maintained) >= 7
}
