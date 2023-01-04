package openssf.omega.policy.recent_security_review

# Metadata (YAML)
# ---
# name: recent_security_review
# title: Subject has had a recent security review (within the last 720 days)
# methodology: >
#   This policy is used to determine if a project has had a security review
#   within the last 720 days (and "passed" it).
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
    input.predicateGenerator.name == "openssf.omega.security_review"
    input.predicateType == "https://github.com/ossf/alpha-omega/security_review/0.1.0"
}

pass := true {
    some assertion in input
    ns := time.parse_rfc3339_ns(input.timestamp)
    d := time.now_ns() - ns
    d < (1000000000 * 60 * 60 * 24 * 720)

    assertion.predicate.pass == true
}
