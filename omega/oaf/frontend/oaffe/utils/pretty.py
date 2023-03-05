LOOKUP = {
    'no_sast_critical_findings': 'No critical findings found through static analysis',
    'no_public_high_vulnerabilities': 'No publicly-known vulnerabilities rated at least "high"',
    'no_public_critical_vulnerabilities': 'No publicly-known vulnerabilities rated "critical"',
    'no_public_vulnerabilities': 'No publicly-known vulnerabilities',
    'no_cryptographic_implementations': 'No cryptographic implementations',
    'no_weak_crypto_algorithms': 'No reference to weak cryptographic algorithms',
    'no_antivirus_findings': 'No viruses detected',
    'reproducible': 'Package can be reliably reproduced',
    'process.is_latest_version': 'Package is the latest version available',
    'process.not_deprecated': 'Package is not deprecated',
    'process.actively_maintained': 'Package is actively maintained',
    'process.code_review': 'Changes are code reviewed',
    'process.has_a_license': 'Has a declared license',


    'openssf.omega.security_advisories': 'Security Advisories',
    'openssf.omega.security_tool_finding': 'Security Tool Findings',
    'openssf.omega.programming_languages': 'Programming Languages',
    'openssf.omega.characteristic': 'Software Characteristics',
    'openssf.omega.metadata': 'Project Metadata',
    'openssf.omega.security_scorecard': 'Security Scorecard',
    'openssf.omega.reproducible': 'Reproducibility',
    'openssf.omega.cryptoimplementation': 'Cryptographic Implementations',
    'openssf.omega.clamav': 'ClamAV Scan Results'
}

def pretty_lookup(key: str) -> str:
    return LOOKUP.get(key, key)

