import subprocess

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
        