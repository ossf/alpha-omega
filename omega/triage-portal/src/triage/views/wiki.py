import json
import os
import uuid
from base64 import b64encode
from typing import Any, List
from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from packageurl import PackageURL

from triage.models import (
    Case,
    Project,
    ProjectVersion,
    WikiArticle,
    WikiArticleRevision,
    WorkItemState,
)
from triage.util.azure_blob_storage import ToolshedBlobStorageAccessor
from triage.util.finding_importers.sarif_importer import SARIFImporter
from triage.util.general import parse_date
from triage.util.search_parser import parse_query_to_Q
from triage.util.source_viewer import path_to_graph
from triage.util.source_viewer.viewer import SourceViewer


@login_required
@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:
    return HttpResponseRedirect("/wiki/home")


@login_required
@require_http_methods(["GET"])
@never_cache
def show_wiki_article_list(request: HttpRequest) -> HttpResponse:
    """Shows all wiki articles."""
    wiki_articles = WikiArticle.active_wiki_articles.all()

    query = request.GET.get("q", "").strip()
    wiki_articles = WikiArticle.objects.all()  # Default
    if query:
        query_object = parse_query_to_Q(WikiArticle, query)
        if query_object:
            wiki_articles = wiki_articles.filter(query_object)

    context = {"query": query, "wiki_articles": wiki_articles}
    return render(request, "triage/wiki_list.html", context)


@login_required
@require_http_methods(["GET"])
def show_wiki_article(
    request: HttpRequest, slug: str, template: str = "triage/wiki_show.html"
) -> HttpResponse:
    """Shows a wiki article (current revision)."""
    article = WikiArticle.objects.filter(slug=slug).first()
    if article:
        context = {
            "wiki_article": article,
            "wiki_article_revision": article.current,
            "wiki_article_states": WorkItemState.choices,
        }
        return render(request, template, context)
    else:
        if slug == "new":
            slug = ""
        context = {
            "wiki_article": {
                "slug": slug,
                "wiki_article_states": WorkItemState.choices,
            }
        }
        return render(request, "triage/wiki_edit.html", context)


def edit_wiki_article(request: HttpRequest, slug: str) -> HttpResponse:
    return show_wiki_article(request, slug, "triage/wiki_edit.html")


@login_required
@require_http_methods(["GET"])
def show_wiki_article_revision(
    request: HttpRequest,
    slug: str,
    wiki_article_revision_uuid: UUID,
    template: str = "triage/wiki_show.html",
) -> HttpResponse:
    """Shows a wiki article (current revision)."""
    article_revision = get_object_or_404(
        WikiArticleRevision, article__slug=slug, uuid=wiki_article_revision_uuid
    )
    context = {
        "wiki_article": article_revision.article,
        "wiki_article_revision": article_revision,
        "wiki_article_states": WorkItemState.choices,
    }
    return render(request, template, context)


def edit_wiki_article_revision(
    request: HttpRequest, slug: str, wiki_article_revision_uuid: UUID
) -> HttpResponse:
    return show_wiki_article_revision(
        request, slug, wiki_article_revision_uuid, "triage/wiki_edit.html"
    )


@login_required
@require_http_methods(["POST"])
def save_wiki_article(request: HttpRequest) -> HttpResponse:
    wiki_article_uuid = request.POST.get("wiki_article_uuid")
    if not wiki_article_uuid:
        wiki_article = WikiArticle()
    else:
        wiki_article = get_object_or_404(WikiArticle, uuid=wiki_article_uuid)

    slug = request.POST.get("slug")
    if not slug:
        slug = slugify(request.POST.get("title"))
    wiki_article.state = request.POST.get("state")
    wiki_article.slug = slug
    wiki_article.save()

    wiki_article_revision = WikiArticleRevision(
        title=request.POST.get("title"),
        content=request.POST.get("content"),
        article=wiki_article,
        change_comment=request.POST.get("change_comment"),
        created_by=request.user,
        updated_by=request.user,
    )
    wiki_article_revision.full_clean()
    wiki_article_revision.save()

    return redirect(wiki_article)
