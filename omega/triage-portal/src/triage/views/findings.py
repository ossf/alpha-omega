import json
import logging
import os
from base64 import b64encode

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from packageurl import PackageURL

from triage.models import (
    Attachment,
    Case,
    File,
    FileContent,
    Finding,
    ProjectVersion,
    Scan,
    WorkItemState,
)
from triage.util.azure_blob_storage import ToolshedBlobStorageAccessor
from triage.util.finding_importers.sarif_importer import SARIFImporter
from triage.util.general import clamp
from triage.util.search_parser import parse_query_to_Q
from triage.util.source_viewer import path_to_graph
from triage.util.source_viewer.viewer import SourceViewer

logger = logging.getLogger(__name__)


@login_required
def show_findings(request: HttpRequest) -> HttpResponse:
    """Shows findings based on a query.

    Params:
        q: query to search for, or all findings if not provided
    """
    query = request.GET.get("q", "").strip()
    page_size = clamp(request.GET.get("page_size", 20), 10, 500)
    page = clamp(request.GET.get("page", 1), 1, 1000)

    findings = Finding.active_findings.all()

    if query:
        findings = Finding.objects.exclude(state=WorkItemState.DELETED)
        query_object = parse_query_to_Q(Finding, query)
        if query_object:
            findings = findings.filter(query_object)

    findings = findings.select_related("project_version", "tool", "file")
    findings = findings.order_by('-project_version__package_url', 'title', 'created_at')
    paginator = Paginator(findings, page_size)
    page_object = paginator.get_page(page)

    query_string = request.GET.copy()
    if 'page' in query_string:
        query_string.pop("page", None)

    context = {"query": query, "findings": page_object, "params": query_string.urlencode() }

    return render(request, "triage/findings_list.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def show_upload(request: HttpRequest) -> HttpResponse:
    """Show the upload form for findings (SARIF, etc.)"""
    if request.method == "GET":
        return render(request, "triage/findings_upload.html")

    if request.method == "POST":
        package_url = request.POST.get("package_url")
        files = request.FILES.getlist("sarif_file[]")

        if not files:
            return HttpResponseBadRequest("No files provided")

        for file in files:
            try:
                importer = SARIFImporter.import_sarif_file(
                    package_url, json.load(file), request.user
                )
            except:  # pylint: disable=bare-except
                logger.warning("Failed to import SARIF file", exc_info=True)

        return redirect("/findings/upload?status=success")


@login_required
def show_finding_by_uuid(request: HttpRequest, finding_uuid) -> HttpResponse:
    finding = get_object_or_404(Finding, uuid=finding_uuid)
    from django.contrib.auth.models import User

    assignee_list = User.objects.all()
    context = {"finding": finding, "assignee_list": assignee_list}
    return render(request, "triage/findings_show.html", context)


@login_required
@require_http_methods(["POST"])
def api_update_finding(request: HttpRequest) -> JsonResponse:
    """Updates a Finding."""

    finding_uuid = request.POST.get("finding_uuid")
    finding = get_object_or_404(Finding, uuid=finding_uuid)
    # if not finding.can_edit(request.user):
    #    return HttpResponseForbidden()

    # Modify only these fields, if provided
    permitted_fields = [
        "analyst_impact",
        "confidence",
        "analyst_severity_level",
        "assigned_to",
        "estimated_impact",
    ]
    is_modified = False
    for field in permitted_fields:
        if field in request.POST:
            value = request.POST.get(field)
            if field == "assigned_to":
                if value == "$self":  # Special case: set to current user
                    value = request.user
                if value == "$clear":  # Special case: clear the field
                    value = None
                else:
                    value = get_user_model().objects.filter(username=value).first()
                    if value is None:
                        continue  # No action, invalid user passed in

            if getattr(finding, field) != value:
                setattr(finding, field, value)
                is_modified = True

    if is_modified:
        finding.save()
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"status": "ok, not modified"})


@login_required
@cache_page(60 * 30)
def api_get_source_code(request: HttpRequest) -> JsonResponse:
    """Returns the source code for a finding."""
    file_uuid = request.GET.get("file_uuid")
    if file_uuid:
        file = File.objects.filter(uuid=file_uuid).select_related("content").first()
        return JsonResponse(
            {
                "file_contents": b64encode(file.content.data).decode("utf-8"),
                "file_name": file.path,
                "status": "ok",
            }
        )
    else:
        logger.info("Source code not found for %s", file_uuid)
        return JsonResponse({"status": "error", "message": "File not found"}, status=404)

    # return JsonResponse({"status": "error"}, status=500)


@login_required
@cache_page(60 * 5)
def api_get_files(request: HttpRequest) -> JsonResponse:
    """Returns a list of files related to a finding."""
    project_version_uuid = request.GET.get("project_version_uuid")
    project_version = get_object_or_404(ProjectVersion, uuid=project_version_uuid)

    source_graph = path_to_graph(
        project_version.files.all(),
        project_version.package_url,
        separator="/",
        root=str(project_version.package_url),
    )

    return JsonResponse({"data": source_graph, "status": "ok"})


# @login_required
# def api_get_file_list(request: HttpRequest) -> JsonResponse:
#    """Returns a list of files in a project."""
#    finding_uuid = request.GET.get("finding_uuid")
#    finding = get_object_or_404(Finding, uuid=finding_uuid)
#    source_code = finding.scan.get_file_list()
#    source_graph = path_to_graph(source_code, finding.scan.project_version.package_url)#
#
#    return JsonResponse({"data": source_graph, "status": "ok"})


@login_required
def api_download_file(request: HttpRequest) -> HttpResponse:
    """Returns a list of files in a project."""
    return HttpResponse("Not implemented.")


@login_required
def api_get_blob_list(request: HttpRequest) -> JsonResponse:
    """Returns a list of files in a project."""
    finding_uuid = request.GET.get("finding_uuid")
    finding = get_object_or_404(Finding, uuid=finding_uuid)
    source_code = finding.scan.get_blob_list()
    source_graph = path_to_graph(
        map(lambda s: s.get("relative_path"), source_code), finding.scan.project_version.package_url
    )

    return JsonResponse({"data": source_graph, "status": "ok"})


@csrf_exempt
@require_http_methods(["POST"])
def api_add(request: HttpRequest) -> JsonResponse:
    """Inserts data into the database.

    Required:
    - sarif => the SARIF content (file contents)
    - package_url => the package URL (must include version)
    - scan_artifact => an archive of the content analyzed
    """
    sarif = request.FILES.get("sarif")
    if sarif is None:
        return JsonResponse({"error": "No sarif provided"})
    sarif_content = json.load(sarif)

    scan_artifact = request.FILES.get("scan_artifact")
    if scan_artifact is None:
        return JsonResponse({"error": "No scan_artifact provided"})

    try:
        package_url = PackageURL.from_string(request.POST.get("package_url"))
        if package_url.version is None:
            raise ValueError("Missing version")
    except ValueError:
        return JsonResponse({"error": "Invalid or missing package url"})

    user = get_user_model().objects.get(pk=1)
    SARIFImporter.import_sarif_file(package_url, sarif_content, user)
    return JsonResponse({"success": True})


@csrf_exempt
@require_http_methods(["POST"])
def api_add_artifact(request: HttpRequest) -> JsonResponse:
    """Inserts data into the database.

    Required:
    - artifact_type => "scan" or "package"
    - action => "add" or "replace" (only used for package)
    - package_url => the package URL (must include version)
    - artifact => file contents to import
    """
    action = request.FILES.get("action")
    if action not in ["add", "update"]:
        return JsonResponse({"error": "Invalid action"})

    artifact_type = request.FILES.get("artifact_type")
    if artifact_type is None:
        return JsonResponse({"error": "No artifact type provided"})

    try:
        package_url = PackageURL.from_string(request.POST.get("package_url"))
        if package_url.version is None:
            raise ValueError("Missing version")
    except ValueError:
        return JsonResponse({"error": "Invalid or missing package url"})

    # TODO: Make this better
    user = get_user_model().objects.get(pk=1)

    if artifact_type == "sarif":
        sarif = request.FILES.get("sarif")
        sarif_content = json.load(sarif)
        SARIFImporter.import_sarif_file(package_url, sarif_content, user)

    """
    Source code files are usually archives that contain source code or other
    artifacts. They'll be automatically extracted during the import process. They
    are associated with a ProjectVersion"""
    if "source_code" in request.FILES:
        source_code = request.FILES.get("source_code")
        source_code_content = source_code.read()
        FileImporter.import_artifact(package_url, source_code_content, user)

    return JsonResponse({"success": True})


def api_upload_attachment(request: HttpRequest) -> JsonResponse:
    """Handles uploads (attachments)"""
    target_type = request.POST.get("target_type")
    target_uuid = request.POST.get("target_uuid")
    if target_uuid is None or target_uuid == "":
        return JsonResponse({"error": "No target_uuid provided"})

    if target_type == "case":
        obj = get_object_or_404(Case, uuid=target_uuid)
    else:
        return JsonResponse({"error": "Invalid target_type"})

    attachments = request.FILES.getlist("attachment")
    results = []
    for attachment in attachments:
        new_attachment = obj.attachments.create(
            filename=attachment.name,
            content_type=attachment.content_type,
            content=attachment.read(),
        )
        results.append({"filename": new_attachment.filename, "uuid": new_attachment.uuid})

    return JsonResponse({"success": True, "attachments": results})
