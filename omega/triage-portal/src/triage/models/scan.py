import logging
import uuid
from typing import Optional

from django.db import models
from django.utils.translation import gettext_lazy as _
from packageurl import PackageURL

from triage.models import BaseTimestampedModel, BaseUserTrackedModel
from triage.util.azure_blob_storage import (
    AzureBlobStorageAccessor,
    ToolshedBlobStorageAccessor,
)
from triage.util.general import modify_purl
from triage.util.source_viewer.viewer import SourceViewer

logger = logging.getLogger(__name__)


class Scan(BaseTimestampedModel, BaseUserTrackedModel):
    """A scan of a project version."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    project_version = models.ForeignKey("ProjectVersion", on_delete=models.CASCADE)
    tool = models.ForeignKey("Tool", on_delete=models.CASCADE)

    artifact_url_base = models.CharField(max_length=1024, null=True, blank=True)
    active = models.BooleanField(default=True)

    files = models.ManyToManyField("File", blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"An execution of {self.tool} against {self.project_version}"

    def get_absolute_url(self):
        return f"/scan/{self.uuid}"

    def get_file_content(self, filename: str) -> Optional[str]:
        if filename is None:
            return None

        accessor = ToolshedBlobStorageAccessor(self)
        for _filename in accessor.get_all_files():
            print(f"Comparing {_filename} to {filename}")
            if _filename == filename:
                return accessor.get_file_content(_filename)
        return None

    def get_source_files(self) -> list:
        """Retreives the source code for this scan."""
        accessor = ToolshedBlobStorageAccessor(self)
        return accessor.get_source_files()

    def get_source_code(self, filename: str) -> Optional[str]:
        """Retreives the source code for a file."""

        viewer = SourceViewer(self.project_version.package_url)
        res = viewer.get_file(filename)
        if res:
            return res.get("content")
        return None

    def get_file_list(self) -> list:
        """Retreives a list of files in the scan."""
        viewer = SourceViewer(self.project_version.package_url)
        return viewer.get_file_list()

    def get_blob_list(self) -> list:
        """Retreives a list of blobs in the scan."""
        purl = PackageURL.from_string(self.project_version.package_url)
        if purl.namespace:
            prefix = f"{purl.type}/{purl.namespace}/{purl.name}/{purl.version}"
        else:
            prefix = f"{purl.type}/{purl.name}/{purl.version}"

        accessor = AzureBlobStorageAccessor(prefix)
        return accessor.get_blob_list()

    def get_file_contents(self, filename) -> Optional[str]:
        """Retreives the contents of a file."""
        accessor = ToolshedBlobStorageAccessor(self)
        return accessor.get_file_contents(filename)

    def get_package_contents(self, filename) -> Optional[str]:
        """Retreives the contents of a file."""
        accessor = ToolshedBlobStorageAccessor(self)
        return accessor.get_package_contents(filename)
