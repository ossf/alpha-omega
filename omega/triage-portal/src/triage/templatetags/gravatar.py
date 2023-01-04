import hashlib
import logging

from django import template

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def gravatar(user, size=128):
    """Convert the user's email address passed in into a gravatar URL."""
    root = "https://gravatar.com/avatar/{0}?r=g&d=mp&s={1}&{2}"
    if user and user.email:
        email = user.email.strip().lower().encode("utf-8")
        # MD5 is mandated by the Gravatar spec - gravatar.com
        hash_value = hashlib.md5(email).hexdigest()  # noqa # nosec
        return root.format(hash_value, str(size), "")
    else:
        # Mystery Person
        return root.format("", str(size), "f=y")
