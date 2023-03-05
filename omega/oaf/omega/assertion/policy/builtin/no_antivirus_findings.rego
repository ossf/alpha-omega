package openssf.omega.policy.no_antivirus_findings

# Metadata (YAML)
# ---
# name: no_antivirus_findings
# title: No findings from anti-virus.
# methodology: >
#   This policy is used to ensure that no viruses are found.
# version: 0.1.0
# last_updated:
#   date: 2023-03-05
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---
import future.keywords.every

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.clamav"
    input.predicateType == "https://github.com/ossf/alpha-omega/clamav/0.1.0"
}

pass := true {
    every assertion in input {
        assertion.predicate.content.infected == 0
    }
}