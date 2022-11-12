package openssf.omega.policy.recent_security_review

# This policy is used to determine if a project has had a recent security review.
#
# VERSION 0.1.0
# LAST UPDATED 2022-11-03 Michael Scovetta

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
