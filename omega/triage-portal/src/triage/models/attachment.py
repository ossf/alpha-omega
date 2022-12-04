import logging
import uuid

from django.db import models

logger = logging.getLogger(__name__)


class Attachment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    filename = models.CharField(max_length=1024)
    content = models.BinaryField()
    content_type = models.CharField(max_length=255)

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return f"/attachment/{self.uuid}"
