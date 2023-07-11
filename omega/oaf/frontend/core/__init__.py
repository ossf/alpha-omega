"""Basic helper functions"""

import os
from django.core.exceptions import ImproperlyConfigured
import django

def get_env_variable(var_name, optional=False):
    """
    Retrieve an environment variable. Any failures will cause an exception
    to be thrown.
    """
    try:
        return os.environ[var_name]
    except KeyError as ex:
        if optional:
            return False
        raise ImproperlyConfigured(
            f"Error: You must set the {var_name} environment variable."
        ) from ex


def to_bool(option: any, default_value: bool = False) -> bool:
    """Convert a value to a bool."""
    if option is None:
        return default_value

    if isinstance(option, bool):
        return option

    try:
        clean = str(option).lower().strip()
        return clean in ["true", "1", "yes", "on"]
    except:
        return default_value
