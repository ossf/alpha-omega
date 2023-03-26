import logging
import requests
from packageurl import PackageURL
from functools import lru_cache

@lru_cache
def get_dependencies(purl: PackageURL) -> dict[str, list[PackageURL]]:
    """Retrieve dependencies from deps.dev."""
    if not purl:
        return None

    if purl.type not in ['npm', 'pypi']:
        logging.warning('Invalid type, not supported by deps.dev.')
        return None

    if purl.namespace:
        url = f'https://deps.dev/_/s/{purl.type}/p/{purl.namespace}/{purl.name}/v/{purl.version}/dependencies'
    else:
        url = f'https://deps.dev/_/s/{purl.type}/p/{purl.name}/v/{purl.version}/dependencies'

    res = requests.get(url, timeout=30)
    res.raise_for_status()
    data = res.json()

    result = {
        'direct': [],
        'indirect': []
    }

    for dependency in data.get('dependencies', []):
        distance = dependency.get('distance', -1)
        if distance < 1:
            continue

        _type = dependency.get('package', {}).get('system', '').lower().strip()
        _name = dependency.get('package', {}).get('name', '').strip()
        _version = dependency.get('version')

        if not _type or not _name or not _version:
            continue

        _dep_purl = str(PackageURL(**{
            'type': _type,
            'name': _name,
            'version': _version
        }))

        if distance == 1:
            result['direct'].append(_dep_purl)
        else:
            result['indirect'].append(_dep_purl)

    return result



