from .base import BaseSARIFAssertion


class NoCriticalSecurityFindingsByTool(BaseSARIFAssertion):
    version = "0.1.0"
    required_args = ["input_file"]

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def filter_lambda(finding):
        tags = ["security", "cwe", "owasp"]
        rule_tags = finding.get("rule_tags", [])
        tag_pass = any([t in rule_tags for t in tags])

        return tag_pass or finding.get("rule_severity", 0) >= 7.0

    def emit(self):
        findings = list(self.enumerate_findings())
        assertion = self.base_assertion()
        assertion["status"] = "pass" if not len(findings) else "fail"
        assertion["predicate"]["critical_findings"] = len(findings)
        return assertion
