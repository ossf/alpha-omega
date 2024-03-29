package openssf.omega.policy.autogenerated.cwe.cwe_553

# Metadata (YAML)
# ---
# name: autogenerated.cwe.cwe_553
# title: "CWE-553: Command Shell in Externally Accessible Directory"
# methodology: >
#   A possible shell file exists in /cgi-bin/ or other accessible directories. This is extremely dangerous and can be used by an attacker to execute commands on the web server.
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
        not "cwe-553" in assertion.predicate.content.tags
    }
}