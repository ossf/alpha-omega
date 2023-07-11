"""Collection of general utility functions."""

import collections.abc
import datetime
import json
import logging
import subprocess  # nosec: B404
import typing
from urllib.parse import urlparse
from urllib3 import Retry
import requests
from requests.adapters import HTTPAdapter
from dateutil.parser import ParserError
from dateutil.parser import parse as _parse_date
from packageurl import PackageURL
from packageurl.contrib.purl2url import purl2url


# From https://github.com/python/cpython/blob/main/Lib/distutils/util.py
# This will be removed in Python 3.12, so we'll keep a copy of it.
# Slightly modified to be more reasonable.
def strtobool(val: any, default_value: bool = False) -> bool:
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    if isinstance(val, bool):
        return val
    val = str(val).strip().lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        return default_value

def get_complex(obj: dict, key: str | list, default_value: typing.Any = ""):
    """Get a value from the dictionary d by nested.key.value.
    If keys contain periods, then use key=['a','b','c'] instead."""
    if not obj or not isinstance(obj, dict):
        return default_value
    _data = obj
    try:
        parts = key.split(".") if isinstance(key, str) else key

        for inner_key in parts:
            _data = _data[inner_key]
        return _data
    except Exception:
        return default_value


def is_command_available(args: list | str):
    """Checks to see if a particular command is available."""
    try:
        if isinstance(args, str):
            args = [args]
        subprocess.run(args, capture_output=True, timeout=10, check=False)  # nosec B603
        return True
    except FileNotFoundError:
        return False


def find_repository(package_url: PackageURL | str) -> str | None:
    """Returns the repository URL for the given package."""
    if not package_url:
        raise EnvironmentError("Invalid PackageURL provided.")

    if isinstance(package_url, str):
        package_url = PackageURL.from_string(package_url)
        if not package_url:
            raise EnvironmentError("Invalid PackageURL provided.")

    if package_url.type == "github":
        try:
            return purl2url(str(package_url))
        except Exception:
            logging.warning("Unable to parse PackageURL to GitHub repository: %s", str(package_url))

    if not is_command_available(["oss-find-source"]):
        raise EnvironmentError("oss-find-source is not available.")

    try:
        cmd = ["oss-find-source", "-S", str(package_url)]
        res = subprocess.run(cmd, check=False, capture_output=True, encoding="utf-8")  # nosec B603
        if res.returncode == 0:
            repository = res.stdout.strip()
            return repository or None
    except Exception:
        logging.warning("Failed to find repository for %s", str(package_url))

    return None


def get_subclasses_recursive(cls):
    """Returns all subclasses of a given class, including subclasses of subclasses."""
    return cls.__subclasses__() + [
        g for s in cls.__subclasses__() for g in get_subclasses_recursive(s)
    ]


def get_package_url_with_version(package_url: PackageURL | str) -> PackageURL:
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
        res = requests.get(f"https://deps.dev/_/s/{purl.type}/p/{purl.name}", timeout=30)

    if res.status_code == 200:
        version = res.json().get("version", {}).get("version")
        if version:
            new_purl = purl.to_dict()
            new_purl["version"] = version
            logging.debug("Latest version is %s", version)
            purl = PackageURL(**new_purl)
            return purl

    # Try using the libraries.io API
    # HACK: Libraries.io knows RubyGems as "pkg:rubygems", nor "pkg:gem", so we need
    #       to convert it to the correct format.
    if purl.type == "gem":
        mod_purl = PackageURL(type="rubygems", name=purl.name, version=purl.version)

    res = subprocess.run([
        "oss-metadata",
        "-s",
        "libraries.io",
        str(mod_purl)
    ], capture_output=True, timeout=10, check=False)  # nosec B603

    if res.returncode == 0:
        data = json.loads(res.stdout)
        latest_version = data.get('latest_release_number')
        if latest_version:
            new_purl = purl.to_dict()
            new_purl["version"] = latest_version
            logging.debug("Latest version is %s", latest_version)
            purl = PackageURL(**new_purl)
            return purl

    raise ValueError("Could not get latest version")

# Source: https://stackoverflow.com/questions/3232943
#         /update-value-of-a-nested-dictionary-of-varying-depth/3233356#3233356
def update_complex(target: dict, overlay: collections.abc.Mapping):
    """Updates a nested dictionary with another nested dictionary."""
    for key, value in overlay.items():
        if isinstance(value, collections.abc.Mapping):
            target[key] = update_complex(target.get(key, {}), value)
        else:
            target[key] = value
    return target


def parse_date(date_string: str, default: typing.Any = None) -> datetime.datetime | typing.Any:
    """Parses a date string into a datetime object."""
    try:
        return _parse_date(date_string)
    except (ParserError, OverflowError):
        return default


# From: https://stackoverflow.com/a/52455972/1384352
def is_valid_url(url: str) -> bool:
    """Checks to see if a URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def encode_path_safe(directory: str) -> str:
    """Replace special characters in a string with valid directory characters (percent encoded)"""
    result = []
    for char in list(directory):
        if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.@":
            result.append(f"%{ord(char):02x}")
        else:
            result.append(char)
    return "".join(result)

def get_requests_session() -> requests.Session:
    """Returns a requests session with a user agent."""
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    return session

class ComplexJSONEncoder(json.JSONEncoder):
    """Handles encoding of complex objects into JSON."""

    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        if isinstance(o, (PackageURL,)):
            return str(o)
        if hasattr(o, "to_json") and callable(o.to_json):
            return o.to_json()
        return super().default(o)
