import hashlib
import base64
import logging
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core import settings
from triage.models import BaseTimestampedModel, BaseUserTrackedModel, WorkItemState

logger = logging.getLogger(__name__)


FILE_TYPES = (
    ("source", _("Source")),
    ("binary", _("Binary")),
    ("other", _("Other")),
    ("unknown", _("Unknown")),
    ("", _("Unknown")),
)


class File(models.Model):
    """
    Represents a file that is associated with an analyzed project.
    """

    class FileType(models.TextChoices):
        SOURCE_CODE = "S", _("Source Code")
        SCAN_RESULT = "R", _("Scan Result")
        UNKNOWN = "U", _("Unknown")

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True, unique=True
    )
    name = models.CharField(max_length=512, db_index=True)
    path = models.CharField(max_length=4096, db_index=True)
    file_type = models.CharField(
        max_length=16, db_index=True, choices=FileType.choices, default=FileType.UNKNOWN
    )
    content_type = models.CharField(max_length=64, db_index=True, null=True, blank=True)
    file_key = models.CharField(max_length=64, db_index=True, null=True, blank=True)

    def __str__(self):
        return str(self.path)


class FileContent(models.Model):
    """Represents file content."""

    hash = models.BinaryField(max_length=32, db_index=True)
    content_type = models.CharField(max_length=64, db_index=True, null=True, blank=True)
    data = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return base64.b64encode(self.hash).decode("ascii")

    @classmethod
    def generate_hash(cls, data: bytes, encode=False) -> str | bytes:
        """Generates a hash for the given data."""
        digest = hashlib.sha256(data, usedforsecurity=True).digest()
        if encode:
            return base64.b64encode(digest).decode("ascii")
        return digest
