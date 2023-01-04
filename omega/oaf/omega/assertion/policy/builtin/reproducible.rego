package openssf.omega.policy.reproducible

# Metadata (YAML)
# ---
# name: reproducible
# title: Subject can be reproduced from its purported source repository.
# methodology: >
#   This policy is used to determine if a package can be rebuilt from its source
#   repository.
# version: 0.1.0
# last_updated:
#   date: 2022-11-16
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---
import future.keywords.in

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.reproducible"
    input.predicateType == "https://github.com/ossf/alpha-omega/reproducible/0.1.0"
}

pass := true {
    some assertion in input
    assertion.predicate.content.reproducible == true
}
