import logging
import uuid

from django.db import models

from triage.models import BaseTimestampedModel, BaseUserTrackedModel, WorkItemState

logger = logging.getLogger(__name__)


class WikiArticleRevision(BaseTimestampedModel, BaseUserTrackedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    article = models.ForeignKey("WikiArticle", on_delete=models.CASCADE, related_name="revisions")
    title = models.CharField(max_length=1024)
    content = models.TextField(null=True, blank=True)
    change_comment = models.CharField(max_length=512, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.article.current = self
        self.article.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/wiki/{self.article.slug}/{self.uuid}"

    def get_absolute_edit_url(self):
        return f"/wiki/{self.article.slug}/{self.uuid}/edit"

    class Meta:
        ordering = ["-created_at"]


class ActiveWikiArticleManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                state__in=[WorkItemState.NEW, WorkItemState.ACTIVE, WorkItemState.NOT_SPECIFIED]
            )
        )


class WikiArticle(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    slug = models.SlugField(unique=True)
    state = models.CharField(
        max_length=2, choices=WorkItemState.choices, default=WorkItemState.ACTIVE
    )
    current = models.ForeignKey(
        WikiArticleRevision, on_delete=models.CASCADE, null=True, blank=True
    )

    active_wiki_articles = ActiveWikiArticleManager()
    objects = models.Manager()

    def __str__(self):
        if self.current:
            return self.current.title
        else:
            return "(No article)"

    def get_absolute_url(self):
        return f"/wiki/{self.slug}"

    def get_absolute_edit_url(self):
        return f"/wiki/{self.slug}/edit"

    @property
    def versions(self):
        return WikiArticleRevision.objects.filter(article=self).order_by("-created_at")

    class Meta:
        ordering = ["slug"]
