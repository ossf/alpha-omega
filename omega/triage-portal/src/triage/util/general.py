import logging
from datetime import datetime

from django.utils import timezone
from django.utils.dateparse import parse_date as django_parse_date
from packageurl import PackageURL

logger = logging.getLogger(__name__)


def get_complex(obj, key, default_value=""):
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


def modify_purl(purl: PackageURL, **kwargs) -> PackageURL:
    """Modify a PackageURL by adding or replacing values in kwargs."""
    return PackageURL(**(purl.to_dict() | kwargs))


def strtobool(value: str, default: bool) -> bool:
    """Convert a string representation of truth to True or False.
    True values are 'y', 'yes', 't', 'true', 'on', and '1';
    False values are 'n', 'no', 'f', 'false', 'off', and '0'.
    Raises ValueError if the string is anything else.
    """
    if isinstance(value, bool):
        return value
    value = str(value).lower()
    if value in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif value in ("n", "no", "f", "false", "off", "0"):
        return False
    return default


def parse_date(date_str: str) -> datetime:
    """Converts a date string to a timezone-aware datetime object."""
    if date_str:
        try:
            parsed = django_parse_date(date_str)
            if parsed:
                parsed_dt = datetime(parsed.year, parsed.month, parsed.day)
                if parsed_dt:
                    return timezone.make_aware(parsed_dt)
        except Exception as msg:
            logger.warning(f"Failed to parse date: {msg}")
    return None

def clamp(value, min_value, max_value):
    """Clamp a value between a minimum and maximum value."""
    return max(min_value, min(float(value), max_value))
