package openssf.omega.policy.no_public_high_vulnerabilities

# Metadata (YAML)
# ---
# name: no_public_high_vulnerabilities
# title: No publicly-known high or critical vulnerabilities exist.
# methodology: >
#   This policy is used to determine if a project contains any publicly-known
#   high or greater vulnerability. "High" is defined by the `openssf.omega.security_advisories`
#   assertion.
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
    input.predicate.generator.name == "openssf.omega.security_advisories"
    input.predicateType == "https://github.com/ossf/alpha-omega/security_advisories/0.1.0"
    input.predicate.content.security_advisories
}

has_critical_findings(x) {
    x.predicate.content.security_advisories.critical
    x.predicate.content.security_advisories.critical > 0
}

has_high_findings(x) {
    x.predicate.content.security_advisories.high
    x.predicate.content.security_advisories.high > 0
}

pass := true {
    every assertion in input {
        not has_high_findings(assertion)
        not has_critical_findings(assertion)
    }
}
