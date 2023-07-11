from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
import uuid
from packageurl import PackageURL


class Subject(models.Model):
    """The subject that we're referring to, normally a PackageURL."""
    SUBJECT_TYPE_PACKAGE_URL = "https://github.com/ossf/alpha-omega/subject/package_url/v0.1"
    SUBJECT_TYPE_GITHUB_URL = "https://github.com/ossf/alpha-omega/subject/github_url/v0.1"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_type = models.CharField(max_length=1024)
    identifier = models.CharField(max_length=1024, db_index=True)

    def __str__(self):
        return f'{self.identifier}'

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'subject_type': self.subject_type,
            'identifier': self.identifier
        }

    def get_versions(self):
        if self.subject_type == self.SUBJECT_TYPE_PACKAGE_URL:
            # Strip version from PackageURL
            purl = PackageURL.from_string(self.identifier).to_dict()
            purl['version'] = None
            purl = str(PackageURL(**purl)) + '@'
            subjects = Subject.objects.filter(subject_type=self.SUBJECT_TYPE_PACKAGE_URL, identifier__startswith=purl)
            return subjects
        else:
            return []

    class Meta:
        ordering = ['subject_type', 'identifier']
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
    name_readable = models.CharField(max_length=1024, null=True, blank=True)
    help_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'version': self.version
        }

class Assertion(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    generator = models.ForeignKey(AssertionGenerator, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.JSONField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.generator}:{self.subject}'

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'generator': self.generator.to_dict(),
            'subject': self.subject.to_dict(),
            'content': self.content,
            'created_date': self.created_date
        }

    class Meta:
        ordering = ['subject']

class Policy(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identifier = models.CharField(max_length=1024)
    name = models.CharField(max_length=1024)
    help_text = models.TextField(null=True, blank=True)
    icon_class = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'identifier': self.identifier,
            'name': self.name
        }

    class Meta:
        verbose_name_plural = "Policies"
        ordering = ['name', 'identifier']

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

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.UNKNOWN)
    evaluated_by = models.CharField(max_length=1024)
    evaluation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subject}:{self.policy}=={self.status}'

    def to_dict(self):
        return {
            'policy': self.policy.to_dict(),
            'subject': self.subject.to_dict(),
            'status': {
                'identifier': self.status,
                'value': self.get_status_display()
            },
            'evaluated_by': self.evaluated_by,
            'evaluated_date': self.evaluation_date
        }

    class Meta:
        ordering = ['evaluation_date']

class PolicyGroup(models.Model):
    """A collection of policies."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    policies = models.ManyToManyField(Policy)
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

class PackageRequest(models.Model):
    """A request to evaluate a package."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    package = models.CharField(max_length=1024)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.package}'

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'package': self.package,
            'active': self.active,
            'created_date': self.created_date
        }

    class Meta:
        ordering = ['created_date']

class PolicyEvaluationQueue(models.Model):
    """An internal queue of packages to be (re-)evaluated against available policies."""

    class Status(models.TextChoices):
        """The status of an item in the refresh queue."""
        NEW = 'N', _('New')
        IN_PROGRESS = 'IP', _('In Progress')
        COMPLETED = 'CO', _('Completed')

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    state = models.CharField(max_length=2, choices=Status.choices, default=Status.NEW)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        ordering = ['updated_date']
        verbose_name_plural = "Refresh Queue Items"
