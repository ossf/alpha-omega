package openssf.omega.policy.no_well_known_backdoors

# Metadata (YAML)
# ---
# name: no_well_known_backdoors
# title: No indicators of well-known backdoors are present.
# methodology: >
#   This policy is used to determine if a project includes indicators of a well-known
#   backdoor.
# version: 0.1.0
# last_updated:
#   date: 2022-11-25
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.oss_detect_backdoor"
    input.predicateType == "https://github.com/ossf/alpha-omega/oss_detect_backdoor/0.1.0"
}

pass := true {
    input.predicate.content.backdoor_present == false
}