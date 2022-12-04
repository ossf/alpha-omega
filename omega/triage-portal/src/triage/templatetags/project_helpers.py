from django import template
from packageurl import PackageURL

register = template.Library()


@register.simple_tag(takes_context=True)
def parse_package_url(context, package_url):
    package_url_obj = PackageURL.from_string(package_url)
    context.update({"package_url": package_url_obj.to_dict()})
    return ""
