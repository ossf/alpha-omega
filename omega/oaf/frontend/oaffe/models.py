from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
import uuid


class Subject(models.Model):
    """The subject that we're referring to, normally a PackageURL."""
    SUBJECT_TYPE_PACKAGE_URL = "https://github.com/ossf/alpha-omega/subject/package_url/v0.1"
    SUBJECT_TYPE_GITHUB_URL = "https://github.com/ossf/alpha-omega/subject/github_url/v0.1"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_type = models.CharField(max_length=1024)
    identifier = models.CharField(max_length=1024, db_index=True)

    def __str__(self):
        return f'{self.identifier}'

    class Meta:
        indexes = [
            models.Index(fields=['subject_type', 'identifier'])
        ]
        constraints = [
            models.UniqueConstraint(name='sti', fields=['subject_type', 'identifier'])
        ]

class AssertionGenerator(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024)
    version = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}@{self.version}'

class Assertion(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    generator = models.ForeignKey(AssertionGenerator, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.JSONField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.generator}:{self.subject}'

class Policy(models.Model):
    identifier = models.CharField(max_length=1024)
    name = models.CharField(max_length=1024)

class PolicyEvaluationResult(models.Model):
    """The result of a policy evaluation."""

    class Status(models.TextChoices):
        """The status of the result of a policy evaluation.

        For example, whether it passed or failed.
        """
        PASSED = 'PA', _('Passed')
        FAILED = 'FA', _('Failed')
        INDETERMINATE = 'IN', _('Indeterminate')
        UNKNOWN = 'UK', _('Unknown')

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.UNKNOWN)
    evaluated_by = models.CharField(max_length=1024)
    evaluation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subject}:{self.policy}=={self.status}'
