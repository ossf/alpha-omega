def normalize_subject(subject: str) -> dict:
    if subject.startswith('https://github.com/ossf/alpha-omega/subject/package_url/v0.1:'):
        short_subject = subject.replace('https://github.com/ossf/alpha-omega/subject/package_url/v0.1:', '')
        return {
            'full': subject,
            'short': short_subject
        }
    else:
        return {
            'full': subject,
            'short': subject
        }
