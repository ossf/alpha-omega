import logging
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from packageurl import PackageURL

from triage.models import BaseTimestampedModel, BaseUserTrackedModel
from triage.models.base import BaseTimestampedModel, BaseUserTrackedModel, WorkItemState
from triage.util.azure_blob_storage import (
    AzureBlobStorageAccessor,
    ToolshedBlobStorageAccessor,
)
from triage.util.general import modify_purl

logger = logging.getLogger(__name__)


class Project(BaseTimestampedModel, BaseUserTrackedModel):
    """An abstract project undergoing analysis."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=1024, db_index=True)
    package_url = models.CharField(max_length=1024, null=True, blank=True, db_index=True)
    metadata = models.JSONField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/projects/{self.uuid}"


class ProjectVersion(BaseTimestampedModel, BaseUserTrackedModel):
    """A version of a project."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    package_url = models.CharField(max_length=1024, null=True, blank=True, db_index=True)
    files = models.ManyToManyField("File", blank=True, editable=True)
    metadata = models.JSONField(null=True)

    def __str__(self):
        return self.package_url

    def get_absolute_url(self):
        return f"/projects/{self.project.uuid}/{self.uuid}"

    @classmethod
    def get_or_create_from_package_url(
        cls, package_url: PackageURL, created_by: User
    ) -> "ProjectVersion":
        """Retrieves or create a PackageVersion from the given package_url."""
        if package_url is None:
            raise ValueError("'package_url' cannot be None.")

        package_url_no_version = modify_purl(package_url, version=None)

        if package_url.namespace:
            package_name = f"{package_url.namespace}/{package_url.name}"
        else:
            package_name = package_url.name

        project, _ = Project.objects.get_or_create(
            package_url=str(package_url_no_version),
            defaults={"name": package_name, "created_by": created_by, "updated_by": created_by},
        )
        project_version, _ = cls.objects.get_or_create(
            project=project,
            package_url=package_url,
            defaults={"created_by": created_by, "updated_by": created_by},
        )
        return project_version
