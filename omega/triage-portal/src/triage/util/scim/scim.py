import uuid
from datetime import datetime, timezone

from triage.models import Finding, Package, PackageVersion, Scan


class ScimManager:
    def __init__(self):
        self.evidence = {}

    def process_all_packages(self):
        for package in Package.objects.filter(active=True):
            self.process_package(package)

    def process_package(self, package: Package):
        SIX_MONTHS_AGO = timezone.now() - datetime.timedelta(days=180)
        latest_scans = (
            Scan.objects.filter(package_version__package=package, analysis_dt__gte=SIX_MONTHS_AGO)
            .order_by("package_version", "-analysis_dt")
            .distinct("package_version")
        )
        evidence = {}
        for scan in latest_scans:
            self.process_scan(scan, evidence)

    def process_scan(self, scan: Scan, evidence: dict):
        tool = scan.tool
        tool_evidence = {
            "id": f"https://scim.openssf.org/v1/tool/{tool.name}/{tool.version}",
            "type": "tool",
            "name": str(scan.tool),
            "externalReferences": [
                {
                    "externalReferenceType": "OTHER",
                    "locator": f"https://omega.openssf.org/tool/{tool.name}/{tool.version}",
                }
            ],
        }
        if tool_evidence not in evidence:
            evidence.append(tool_evidence)

        if scan.findings.filter(severity=Finding.SeverityLevel.VERY_HIGH).count() == 0:
            evidence.append(
                {
                    "id": uuid.uuid4().hex,
                    "type": "Claim",
                    "claimant": "https://scim.openssf.org/v1/tool/{tool.name}/{tool.version}",
                    "subjects": [scan.project_version.package_url],
                    "predicateType": "https://scim.openssf.org/v1/types/predicate/conformance",
                    "predicate": {
                        "requirement": f"https://omega.openssf.org/scim/requirement/{tool.name}/no-very-high-severity-findings",
                    },
                }
            )

        if (
            scan.findings.filter(
                severity__in=[
                    Finding.SeverityLevel.VERY_HIGH,
                    Finding.SeverityLevel.HIGH,
                    Finding.SeverityLevel.MEDIUM,
                ]
            ).count()
            == 0
        ):
            evidence.append(
                {
                    "id": uuid.uuid4().hex,
                    "type": "Claim",
                    "claimant": "https://scim.openssf.org/v1/tool/{tool.name}/{tool.version}",
                    "subjects": [scan.project_version.package_url],
                    "predicateType": "https://scim.openssf.org/v1/types/predicate/conformance",
                    "predicate": {
                        "requirement": f"https://omega.openssf.org/scim/requirement/{tool.name}/no-medium-or-higher-severity-findings",
                    },
                }
            )

        package_version = scan.package_version
        findings = Finding.objects.filter(package_version=package_version)
        self.process_findings(findings)
