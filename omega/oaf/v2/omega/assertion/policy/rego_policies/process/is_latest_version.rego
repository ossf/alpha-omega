package openssf.omega.policy.process.actively_maintained

# This policy is used to determine if a project is the latest version.
#
# VERSION 0.1.0
# LAST UPDATED 2022-11-16 Michael Scovetta

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.metadata"
    input.predicateType == "https://github.com/ossf/alpha-omega/v0.1"
}

pass := true {
    input.predicate.content.metadata.is_latest_version == true
}
