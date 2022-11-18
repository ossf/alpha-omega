package openssf.omega.policy.process.code_review

# Metadata (YAML)
# ---
# title: Code review usually takes place.
# methodology: >
#   This policy is used to determine if code review usually takes place, based on
#   the uses the openssf.omega.security_scorecards assertion, which itself is based on
#   the OpenSSF Security Scorecards project.
# version: 0.1.0
# last_updated:
#   date: 2022-11-11
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.security_scorecards"
    input.predicateType == "https://github.com/ossf/alpha-omega/v0.1"
}

pass := true {
    input.predicate.content.scorecard_data.code_review >= 7
}
