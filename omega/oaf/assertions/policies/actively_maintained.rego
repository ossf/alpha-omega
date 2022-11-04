package openssf.omega.policy.actively_maintained

# This policy is used to determine if a project is actively maintained.
# The logic is as follows:
# 1. If the project has any change in the last 6 months, it is actively maintained.
# 2. Else if the project has any code change in the last 12 months, it is actively maintained.
# 3. Else it is not actively maintained.
#
# VERSION 0.1.0
# LAST UPDATED 2022-11-03 Michael Scovetta

default pass = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicateGenerator.name == "openssf.omega.actively_maintained"
}

is_correct_predicate_type {
    input.predicateType == "https://github.com/ossf/alpha-omega/v0.1"
}

pass := true {
    input.predicate.updated_at

	ns := time.parse_rfc3339_ns(input.predicate.updated_at) 
	d := time.now_ns() - ns
    
    is_correct_predicate_type
    
    d < (1000000000 * 60 * 60 * 24 * 180)
} {
    input.predicate.pushed_at

	ns := time.parse_rfc3339_ns(input.predicate.pushed_at) 
	d := time.now_ns() - ns
    is_correct_predicate_type
    d < (1000000000 * 60 * 60 * 24 * 365)
}
