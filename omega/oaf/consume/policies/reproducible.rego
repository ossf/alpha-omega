package openssf.omega.policy.reproducible

# This policy is used to determine if a project is reproducible.
#
# VERSION 0.1.0
# LAST UPDATED 2022-11-03 Michael Scovetta

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.reproducible"
    input.predicateType == "https://github.com/ossf/alpha-omega/v0.1"
}

pass := true {
    input.predicate.content.reproducible == true
}
