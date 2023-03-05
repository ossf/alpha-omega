from django.db import models
from django.urls import reverse
import uuid

class Assertion(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    generator = models.CharField(max_length=1024)
    subject = models.CharField(max_length=1024)
    content = models.JSONField()
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.generator}:{self.subject}'

class Policy(models.Model):
    subject = models.CharField(max_length=1024)
    policy = models.CharField(max_length=1024)
    status = models.BooleanField()
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subject}:{self.policy}=={self.status}'
