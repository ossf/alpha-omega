import logging
import os
import shutil
import subprocess
import tempfile
from typing import Callable, List

from django.core.cache import cache

from core.settings import OSSGADGET_PATH
from triage.util.source_viewer.pathsimilarity import PathSimilarity

logger = logging.getLogger(__name__)

"""
Usage:
u = SourceViewer("pkg:npm/left-pad@1.3.0")
file = u.get_file("/index.js")
files = u.find_files(u => u.name == "index.js")
file = u.get_files()
"""


class SourceViewer:
    def __init__(self, package_url):
        self.package_url = str(package_url)

    def load_if_needed(self):
        """Call OSS-Download to retrieve the package, extract it, and the load it into memory."""
        if cache.get(f"sv_{self.package_url}_exists") == 1:
            return

        logger.debug("Loading source for package %s", self.package_url)

        with tempfile.TemporaryDirectory() as temp_directory:
            res = subprocess.run(
                ["./oss-download", "-e", "-x", temp_directory, self.package_url],
                capture_output=True,
                cwd=OSSGADGET_PATH,
            )
            if res.returncode != 0 or not os.listdir(temp_directory):
                logger.debug("Failed to load source for package %s", self.package_url)
                raise Exception("Failed to download package")

            cache_updates = {
                f"sv_{self.package_url}_exists": 1,
                f"sv_{self.package_url}_files": set(),
            }
            for root, dirs, files in os.walk(temp_directory):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = full_path[len(temp_directory) + 1 :].replace("\\", "/")
                    cache_updates[f"sv_{self.package_url}_files"].add(relative_path)
                    with open(full_path, "rb") as f:
                        file_cache_key = f"sv_{self.package_url}_{relative_path}"
                        cache_updates[file_cache_key] = f.read()
            logger.debug(
                "Adding %d entries to cache", len(cache_updates[f"sv_{self.package_url}_files"])
            )
            cache.set_many(cache_updates, timeout=60 * 60 * 8)
            self._is_loaded = True

    def get_file(self, file_path: str) -> dict:
        logger.debug("get_file(%s)", file_path)
        if not file_path:
            return None

        self.load_if_needed()

        target_path = PathSimilarity.find_most_similar_path(self.get_file_list(), file_path)
        if target_path:
            return {
                "path": target_path,
                "content": cache.get(f"sv_{self.package_url}_{target_path}"),
            }
        else:
            return None

    def get_file_list(self):
        self.load_if_needed()
        return cache.get(f"sv_{self.package_url}_files")

    def get_files(self):
        return self.find_files(lambda u, c: True)

    def find_files(self, lambda_filter: Callable[[str], str]) -> List[dict]:
        self.load_if_needed()

        file_list = cache.get(f"sv_{self.package_url}_files")
        for file_path in file_list:
            print(file_path)
            if lambda_filter(file_path):
                yield {
                    "path": file_path,
                    "content": cache.get(f"sv_{self.package_url}_{file_path}"),
                }
