"""Identifies whether a given package has security findings."""

from .base import BaseSARIFAssertion


class SecurityFindingsByTool(BaseSARIFAssertion):
    """Identifies whether a given package has security findings."""

    required_args = ["input_file"]

    class Meta:
        """
        Metadata for the assertion.
        """

        name = "openssf.omega.tool_security_findings"
        version = "0.1.0"

    @staticmethod
    def filter_lambda(finding):
        """Filters a particular finding based on the finding's tags and severity."""
        tags = ["security", "cwe", "owasp"]
        rule_tags = finding.get("rule_tags", [])
        tag_pass = any([t in rule_tags for t in tags])

        return tag_pass or finding.get("rule_severity", 0) >= 7.0

    def emit(self):
        """Emits a security finding assertion for the targeted package."""
        findings = list(self.enumerate_findings())
        assertion = self.base_assertion()
        assertion["status"] = "pass" if findings else "fail"
        assertion["predicate"]["critical_findings"] = len(findings)
        return assertion
