package openssf.omega.policy.no_polynomial_redos

# Metadata (YAML)
# ---
# name: no_polynomial_redos
# title: No polynomial regular expression denial of service vulnerabilities
# methodology: >
#   This policy is used to determine if a project contains any polynomial
#   regular expression denial of service vulnerabilities
# version: 0.1.0
# last_updated:
#   date: 2023-05-19
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---

import future.keywords.every

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.security_tool_finding"
    input.predicateType == "https://github.com/ossf/alpha-omega/security_tool_finding/0.1.0"
    input.predicate.content.category
}

has_findings(x) {
    x.predicate.content.category["github:codeql:js/polynomial-redos"] > 0
}

pass := true {
    every assertion in input {
        not has_findings(assertion)
    }
}
