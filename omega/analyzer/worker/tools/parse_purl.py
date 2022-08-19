# Copyright (C) Microsoft Corporation, All rights reserved.

import sys
from packageurl import PackageURL
import urllib

if len(sys.argv) != 2:
    sys.exit(1)

purl = sys.argv[1]
try:
    purl_obj = PackageURL.from_string(purl)
    
    if not purl_obj.version:
        raise Exception("Missing version.")
    if not purl_obj.type:
        raise Exception("Missing type.")
    if not purl_obj.name:
        raise Exception("Missing name.")

    for k, v in purl_obj.to_dict().items():
        if k == 'qualifiers': continue
        print("PACKAGE_{0}:{1}".format(k.upper(), v or ''))
        print("PACKAGE_{0}_ENCODED:{1}".format(k.upper(), urllib.parse.quote(v or '').replace('/', '%2F')))
    for k, v in purl_obj.qualifiers.items():
        print("PACKAGE_QUALIFIER_{0}:{1}".format(k.upper(), v or ''))
        print("PACKAGE_QUALIFIER_{0}_ENCODED:{1}".format(k.upper(), urllib.parse.quote(v or '').replace('/', '%2F')))
    print("PACKAGE_PURL:{0}".format(purl_obj.to_string()))
    noversion = PackageURL(type=purl_obj.type, namespace=purl_obj.namespace, name=purl_obj.name, version=None, qualifiers=purl_obj.qualifiers, subpath=purl_obj.subpath)
    print("PACKAGE_PURL_NOVERSION:{0}".format(noversion.to_string()))
    
    _dir = filter(lambda s: s, [purl_obj.type, purl_obj.namespace, purl_obj.name, purl_obj.version])
    print("PACKAGE_DIR:{0}".format('/'.join(_dir)))
    
    if purl_obj.namespace:
        print("PACKAGE_NAMESPACE_NAME_ENCODED:{0}".format(urllib.parse.quote(purl_obj.namespace + "/" + purl_obj.name).replace('/', '%2F')))
        print("PACKAGE_NAMESPACE_NAME:{0}".format(purl_obj.namespace + "/" + purl_obj.name))
    else:
        print("PACKAGE_NAMESPACE_NAME_ENCODED:{0}".format(urllib.parse.quote(purl_obj.name).replace('/', '%2F')))
        print("PACKAGE_NAMESPACE_NAME:{0}".format(purl_obj.name))

    _dir = filter(lambda s: s, [noversion.type, noversion.namespace, noversion.name, noversion.version])
    print("PACKAGE_DIR_NOVERSION:{0}".format('/'.join(_dir)))

except Exception as msg:
    print(msg)
    print("ERROR: Unable to parse Package URL.")
    sys.exit(1)

