package openssf.omega.policy.recent_security_review

# Metadata (YAML)
# ---
# title: Subject is marked as deprecated.
# methodology: >
#   This policy is used to determine if a project is deprecated, based on
#   the openssf.omega.metadata assertion.
# version: 0.1.0
# last_updated:
#   date: 2022-11-16
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---

default pass = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicateGenerator.name == "openssf.omega.manual_security_review"
    input.predicateType == "https://github.com/ossf/alpha-omega/v0.1"
}

pass := true {
	ns := time.parse_rfc3339_ns(input.timestamp)
	d := time.now_ns() - ns
    d < (1000000000 * 60 * 60 * 24 * 720)

    input.predicate.pass == true
}
