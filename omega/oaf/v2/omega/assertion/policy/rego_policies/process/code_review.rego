package openssf.omega.policy.process.code_review

# This policy is used to determine if a project uses a code review process.
# Logic is delegated to the OpenSSF Security Scorecards project.
#
# VERSION 0.1.0
# LAST UPDATED 2022-11-12 Michael Scovetta

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
