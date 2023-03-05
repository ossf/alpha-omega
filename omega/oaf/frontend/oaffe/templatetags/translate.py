import hashlib
import logging

from django import template
from oaffe.utils.pretty import LOOKUP

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def translate(text):
    """Translate the text passed in."""
    return LOOKUP.get(text, text)

@register.filter
def short_name(text):
    try:
        p = text.split(':', 2)[2:][0]
        return p
    except:
        return text