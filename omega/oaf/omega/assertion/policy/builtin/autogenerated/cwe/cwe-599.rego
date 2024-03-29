package openssf.omega.policy.autogenerated.cwe.cwe_599

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_599
# title: "CWE-599: Missing Validation of OpenSSL Certificate"
# methodology: >
#   The product uses OpenSSL and trusts or uses a certificate without using the SSL_get_verify_result() function to ensure that the certificate satisfies all necessary security requirements.
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
        not "cwe-599" in assertion.predicate.content.tags
    }
}