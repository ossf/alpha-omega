package openssf.omega.policy.no_sast_critical_findings

# Metadata (YAML)
# ---
# name: no_sast_critical_findings
# title: No critical findings from a SAST tool
# methodology: >
#   This policy is used to determine if a project contains any critical
#   vulnerabilities evidenced by a security tool finding.
# version: 0.1.0
# last_updated:
#   date: 2022-12-10
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---

import future.keywords.every

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.security_tool_finding"
    input.predicateType == "https://github.com/ossf/alpha-omega/security_tool_finding/0.1.0"
    input.predicate.content.severity
}

has_critical_findings(x) {
    x.predicate.content.severity.critical
    x.predicate.content.severity.critical > 0
}

pass := true {
    every assertion in input {
        not has_critical_findings(assertion)
    }
}
