# -*- coding: utf-8 -*-
"""
This file is required so that individual modules can be referenced from files within
this directory.
"""

from triage.models.attachment import Attachment

# import triage.models.project
# import triage.models.tool_defect
from triage.models.base import BaseTimestampedModel, BaseUserTrackedModel, WorkItemState
from triage.models.case import Case
from triage.models.File import File, FileContent
from triage.models.filter import Filter
from triage.models.finding import Finding
from triage.models.note import Note
from triage.models.project import Project, ProjectVersion
from triage.models.scan import Scan
from triage.models.tool import Tool
from triage.models.tool_defect import ToolDefect
from triage.models.triage import TriageRule
from triage.models.wiki import WikiArticle, WikiArticleRevision

# class File(models.Model):
#    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    scan = models.ForeignKey(Scan, on_delete=models.CASCADE)#

#    content = models.FileField(upload_to="file_archive")
#    content_hash = models.CharField(max_length=128, db_index=True)
#    path = models.CharField(max_length=4096)
