package openssf.omega.policy.autogenerated.cwe.cwe_601

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_601
# title: "CWE-601: URL Redirection to Untrusted Site ('Open Redirect')"
# methodology: >
#   A web application accepts a user-controlled input that specifies a link to an external site, and uses that link in a Redirect. This simplifies phishing attacks.
# version: 0.1.0
# last_updated:
#   date: 2023-05-25
#   author: Michael Scovetta <michael.scovetta@gmail.com>
# ---

import future.keywords.every
import future.keywords.in

default pass = false
default applies = false

# Identify whether this policy applies to a given data object
applies := true {
    input.predicate.generator.name == "openssf.omega.security_tool_finding"
    input.predicateType == "https://github.com/ossf/alpha-omega/security_tool_finding/0.1.0"
    input.predicate.content.tags
}

pass := true {
    every assertion in input {
        not "cwe-601" in assertion.predicate.content.tags
    }
}