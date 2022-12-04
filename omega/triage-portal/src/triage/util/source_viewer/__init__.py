import logging

from django.db.models.query import QuerySet

logger = logging.getLogger(__name__)

"""
Example:
input:
["/foo", "/foo/bar", "/foo/bar/baz"]
output:
[{
    id: "/foo"
    full_path: "/foo"
]

"""


def path_to_graph(files: QuerySet, package_url, separator="/", root=None):
    """
    Converts a list of paths into a graph suitable for jstree.

    Args:
        paths: list of paths
        separator: path separator
        root: root directory to pin the graph to

    Returns:
     a list of dictionaries containing the relevant
     fields for jstree.
    """
    if not files:
        return []

    result = []
    seen_nids = set()
    if root:
        result.append(
            {
                "id": root,  # TODO minimize this via a lookup table
                "full_path": "#",
                "text": root,
                "parent": "#",
                "package_url": None,
                "path": "/",
                "file_id": None,
                "icon": "fa fa-folder",
            }
        )
    else:
        root = "#"

    for file in files:
        path = file.path
        if not isinstance(path, str) or not path or path.startswith("pkg:"):
            logger.debug("Ignoring invalid path [%s]", path)
            continue

        if not path.startswith(separator):
            path = separator + path

        path_parts = path.split(separator)[1:]

        logging.debug(f"Analyzing: %s", path_parts)
        for (part_id, part) in enumerate(path_parts):
            if part_id == 0:
                parent_id = root
                node_id = part
            else:
                parent_id = separator.join(path_parts[:part_id])
                node_id = separator.join(path_parts[: (part_id + 1)])
            node_name = part

            if node_name and node_id not in seen_nids:
                result.append(
                    {
                        "id": node_id,  # TODO minimize this via a lookup table
                        "full_path": node_id,
                        "text": node_name,
                        "parent": parent_id,
                        "package_url": package_url,
                        "file_uuid": file.uuid,
                        "li_attr": {"package_url": package_url},
                        "path": node_id,
                        "icon": get_icon_for_path(node_name, part_id == len(path_parts)),
                    }
                )
                seen_nids.add(node_id)
    return result


def get_icon_for_path(path: str, is_leaf_node: bool) -> str:
    # if not is_leaf_node:
    #    return "fa fa-folder"

    icon_map = {
        "application/javascript": "fa fa-code",
        "text/x-python": "fa fa-code",
        "application/json": "fa fa-code",
        "text/html": "fab fa-html5",
        "text/css": "fab fa-css3",
        "text/markdown": "fab fa-markdown",
        "text/plain": "fas fa-file-alt",
        "application/pdf": "fas fa-file-pdf",
        "application/zip": "far fa-file-archive",
        "application/x-tar": "far fa-file-archive",
        "text/csv": "fas fa-file-csv",
    }
    extension_map = {
        ".cs": "fa fa-code",
        ".log": "far fa-file-alt",
        ".gz": "fa fa-file-archive",
        ".error": "fas fa-exclamation-triangle",
        ".sarif": "fas fa-bug",
    }
    import mimetypes

    for mime_type, css in icon_map.items():
        if mimetypes.guess_type(path)[0] == mime_type:
            return css

    for extension, css in extension_map.items():
        if path.endswith(extension):
            return css

    if "." not in path:
        return "far fa-folder-open"

    return "fa fa-file-alt"  # fallback, default
