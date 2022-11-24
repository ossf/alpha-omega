"""Collection of general utility functions."""

import collections.abc
import logging
import subprocess  # nosec: B404
import typing
import datetime
from dateutil.parser import parse as _parse_date
from dateutil.parser import ParserError
from urllib.parse import urlparse

import requests
from packageurl import PackageURL
from packageurl.contrib.purl2url import purl2url


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


def get_complex(obj: dict, key: str | list, default_value: typing.Any =""):
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
        return purl2url(package_url)

    if not is_command_available(["oss-find-source"]):
        raise EnvironmentError("oss-find-source is not available.")

    cmd = ["oss-find-source", "-S", str(package_url)]
    res = subprocess.run(cmd, check=False, capture_output=True, encoding="utf-8")  # nosec B603
    if res.returncode == 0:
        repository = res.stdout.strip()
        return repository or None

    return None


def get_subclasses_recursive(cls):
    """Returns all subclasses of a given class, including subclasses of subclasses."""
    return cls.__subclasses__() + [
        g for s in cls.__subclasses__() for g in get_subclasses_recursive(s)
    ]


def get_package_url_with_version(package_url: PackageURL | str) -> str:
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