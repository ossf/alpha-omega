# -*- coding: utf-8 -*-
"""This module URL patterns specific to the Triage Portal."""

from django.urls import path

from triage.views import attachments, cases, filters, findings, home, tool_defect, wiki

urlpatterns = [
    # Cases
    path("cases/<uuid:case_uuid>", cases.show_case),
    path("cases/new", cases.new_case),
    path("cases/save", cases.save_case),
    path("cases/", cases.show_cases),
    # Tooling Defects
    path("tool_defect/<uuid:tool_defect_uuid>", tool_defect.show_tool_defect),
    path("tool_defect/new", tool_defect.show_add_tool_defect),
    path("tool_defect/save", tool_defect.save_tool_defect),
    path("tool_defect/", tool_defect.show_tool_defects),
    # Findings
    path("api/findings/add_archive", findings.api_add_scan_archive),
    path("api/findings/get_files", findings.api_get_files),
    path("api/findings/get_source_code", findings.api_get_source_code),
    path("api/findings/download_file", findings.api_download_file),
    path("api/upload", findings.api_upload_attachment),
    # path("api/findings/get_file_list", findings.api_get_file_list),
    path("api/findings/get_blob_list", findings.api_get_blob_list),
    path("api/1/findings/update", findings.api_update_finding),
    # Attachments
    path("attachment/<uuid:attachment_uuid>", attachments.download_attachment),
    path("findings/<uuid:finding_uuid>", findings.show_finding_by_uuid),
    path("findings/upload", findings.show_upload),
    path("findings/", findings.show_findings),
    # Filters
    path("filter/<uuid:filter_uuid>", filters.show_filter),
    path("filter/new", filters.new_filter),
    path("filter/save", filters.save_filter),
    path("filter/execute", filters.execute_filter),
    path("filter/delete", filters.delete_filter),
    path("filter/", filters.show_filters),
    # Wiki
    path("wiki/special:list", wiki.show_wiki_article_list),
    path("wiki/save", wiki.save_wiki_article),
    path("wiki/<str:slug>", wiki.show_wiki_article),
    path("wiki/<str:slug>/<uuid:wiki_article_revision_uuid>", wiki.show_wiki_article_revision),
    path("wiki/<str:slug>/edit", wiki.edit_wiki_article),
    path("wiki/<str:slug>/<uuid:wiki_article_revision_uuid>/edit", wiki.edit_wiki_article_revision),
    path("wiki/", wiki.home),
    # Default (Home)
    path("", home.home),
]
