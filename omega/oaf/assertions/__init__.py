import subprocess
import logging
from typing import Union
from packageurl import PackageURL
import requests

# From https://github.com/python/cpython/blob/main/Lib/distutils/util.py
# This will be removed in Python 3.12, so we'll keep a copy of it.
def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    elif val in ("n", "no", "f", "false", "off", "0"):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))

def is_command_available(args):
    """Checks to see if a particular command is available."""
    try:
        subprocess.run(args, capture_output=True, timeout=10, check=False)
        return True
    except FileNotFoundError:
        return False

def get_package_url_with_version(package_url: Union[PackageURL, str]) -> str:
    """Adds the latest version to a versionless PackageURL."""
    logging.debug('Getting latest version for "%s"', str(package_url))
    if isinstance(package_url, str):
        purl = PackageURL.from_string(package_url)
    elif isinstance(package_url, PackageURL):
        purl = package_url
    else:
        raise TypeError("package_url must be a string or PackageURL")

    if purl.version:
        return purl

    if purl.namespace:
        res = requests.get(
            f"https://deps.dev/_/s/{purl.type}/p/{purl.namespace}/{purl.name}",
            timeout=30,
        )
    else:
        res = requests.get(
            f"https://deps.dev/_/s/{purl.type}/p/{purl.name}", timeout=30
        )

    if res.status_code == 200:
        version = res.json().get("version", {}).get("version")
        if version:
            new_purl = purl.to_dict()
            new_purl["version"] = version
            logging.debug("Latest version is %s", version)
            purl = PackageURL(**new_purl)
            return purl
    raise ValueError("Could not get latest version")
