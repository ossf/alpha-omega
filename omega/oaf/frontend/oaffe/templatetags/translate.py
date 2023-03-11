import hashlib
import logging
from packageurl import PackageURL
from oaffe.models import Subject
from django import template
from oaffe.utils.pretty import LOOKUP

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def translate(text):
    """Translate the text passed in."""

    return LOOKUP.get(text, text)

@register.filter
def format_subject(subject: Subject, arg):
    if subject.subject_type == Subject.SUBJECT_TYPE_PACKAGE_URL:
        purl = PackageURL.from_string(subject.identifier)
        if arg == "full_name":
            if purl.namespace:
                return f'{purl.namespace}/{purl.name}'
            else:
                return purl.name

        if hasattr(purl, arg):
            return getattr(purl, arg)

    return str(subject)