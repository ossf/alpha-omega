import json
import logging
import os
import re
from functools import lru_cache

from azure.storage.blob import BlobProperties, BlobServiceClient
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from packageurl import PackageURL

from core.settings import (
    TOOLSHED_BLOB_STORAGE_CONTAINER_SECRET,
    TOOLSHED_BLOB_STORAGE_URL_SECRET,
)
from triage.models import ProjectVersion, Scan, Tool
from triage.util.finding_importers.file_importer import FileImporter
from triage.util.finding_importers.sarif_importer import SARIFImporter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Imports a project from the Toolshed repository"

    def add_arguments(self, parser):
        """Assembles arguments to the command."""
        parser.add_argument("--package", required=False, type=str, help="URL (PackageURL format)")
        parser.add_argument(
            "--import-all", required=False, action="store_true", help="SARIF file to load"
        )
        parser.add_argument(
            "--maximum",
            required=False,
            type=int,
            help="Maximum number of entries to import",
            default=0,
        )

    @classmethod
    def prefix_for_package_url(self, package_url_str: str) -> str:
        try:
            package_url = PackageURL.from_string(package_url_str)
            if package_url.namespace:
                prefix = f"{package_url.type}/{package_url.namespace}/{package_url.name}/{package_url.version}"
            else:
                prefix = f"{package_url.type}/{package_url.name}/{package_url.version}"
        except ValueError:
            prefix = None

        return prefix

    def handle(self, *args, **options):
        """Handle the 'import sarif' command."""
        package = options.get("package")
        if not package and not options.get("import_all"):
            raise ValueError("Must specify either --package or --import-all")

        sarif_importer = SARIFImporter()

        self.initialize_toolshed()
        user = get_user_model().objects.get(pk=1)
        scan_map = {}

        if package:
            prefix = Command.prefix_for_package_url(package)
            blobs = self.container.list_blobs(name_starts_with=prefix)
        elif options.get("import_all"):
            package_url = None
            blobs = self.container.list_blobs(
                name_starts_with="npm",
            )  # TODO: temporary
        else:
            raise ValueError("Must specify either --package or --import-all")

        num_imported = 0
        for blob in blobs:  # type: BlobProperties
            print(f"Importing {blob.name}")
            num_imported += 1
            if num_imported > options.get("maximum", 0) > 0:
                logger.info("Maximum number of entries reached")
                break

            package_url = Command.filename_to_package_url(blob.name)

            # match = re.match(r".*/tool-([^\.]+)\.sarif", blob.name, re.IGNORECASE)
            # if not match:
            #    logger.info(f"Skipping {blob.name}")
            #    continue
            # tool_name = match.group(1)
            project_version = ProjectVersion.get_or_create_from_package_url(package_url, user)

            # Each tool result is a separate scan
            # scan = Scan(
            #    project_version=project_version,
            #    tool=Tool.objects.get_or_create(name=tool_name)[0],
            #    created_by=user,
            #    updated_by=user,
            # )
            # scan.save()

            file_importer = FileImporter()

            if blob.name.endswith(".sarif"):
                logger.debug("Importing %s", blob.name)
                try:
                    blob_contents = self.container.download_blob(blob.name).content_as_text()
                    sarif = json.loads(blob_contents)
                    SARIFImporter.import_sarif_file(package_url, sarif, user)
                    FileImporter.import_file(
                        f"tool/{os.path.basename(blob.name)}",
                        blob.name,
                        blob_contents.encode("utf-8", errors="ignore"),
                        user,
                    )
                except Exception as msg:
                    logger.error("Unable to import %s: %s", blob.name, msg, exc_info=True)
                    continue

            elif "/reference-binaries/" in blob.name:
                print(f"Importing {blob.name}")
                logger.debug("Importing %s", blob.name)
                try:
                    blob_contents = self.container.download_blob(blob.name).content_as_bytes()
                    FileImporter.import_file(
                        f"src/{blob.name}", blob.name, blob_contents, project_version
                    )
                except Exception as msg:
                    logger.error("Unable to import %s: %s", blob.name, msg, exc_info=True)
                    continue

    @classmethod
    @lru_cache
    def filename_to_package_url(cls, filename):
        """Convert a filename to a PackageURL."""
        print(filename)
        match = re.match(
            r"^(?P<type>[^/]+)/(?P<namespace>[^/]+)/(?P<name>[^/]+)/(?P<version>[^/]+)/(reference-binaries|summary-|tool-|admin-).*$",
            filename,
        )
        print(f"Match={bool(match)}")
        if not match:
            match = re.match(
                r"^(?P<type>[^/]+)/(?P<name>[^/]+)/(?P<version>[^/]+)/(reference-binaries|summary-|tool-|admin-).*$",
                filename,
            )
        if not match:
            logger.debug("Unable to parse filename [%s]", filename)
            return None

        try:
            package_url = PackageURL(
                type=match.group("type"),
                namespace=match.group("namespace") if "namespace" in match.groupdict() else None,
                name=match.group("name"),
                version=match.group("version"),
            )
            print(package_url)
            return package_url
        except Exception as msg:
            logger.debug("Unable to create PackageURL from %s: %s", filename, msg)
            return None

    def initialize_toolshed(self):
        if not TOOLSHED_BLOB_STORAGE_URL_SECRET or not TOOLSHED_BLOB_STORAGE_CONTAINER_SECRET:
            raise ValueError("TOOLSHED_BLOB_STORAGE_URL and TOOLSHED_BLOB_CONTAINER must be set")

        self.blob_service = BlobServiceClient(TOOLSHED_BLOB_STORAGE_URL_SECRET)

        self.container = self.blob_service.get_container_client(
            TOOLSHED_BLOB_STORAGE_CONTAINER_SECRET
        )
