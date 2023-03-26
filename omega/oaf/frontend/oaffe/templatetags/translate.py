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
    if isinstance(subject, Subject):
        if subject.subject_type == Subject.SUBJECT_TYPE_PACKAGE_URL:
            subject = str(subject.identifier)

    if isinstance(subject, str):
        purl = PackageURL.from_string(subject)
        if arg == "full_name":
            if purl.namespace:
                return f'{purl.namespace}/{purl.name}'
            else:
                return purl.name

        if hasattr(purl, arg):
            return getattr(purl, arg)

    return str(subject)

@register.filter
def shorten_version(text):
    if len(text) == 40:
        return text[0:6]
    return text

@register.filter
def abbrev(policy):
    if not policy:
        return None
    text = policy.name
    if not text:
        text = policy.identifier

    text = text.replace("-", " ").replace("_", " ").replace('.', ' ')
    return ''.join([t[0] for t in text.split() if t[0]]).upper()