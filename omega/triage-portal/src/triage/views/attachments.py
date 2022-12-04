import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from triage.models import Attachment


@login_required
@require_http_methods(["GET"])
def download_attachment(request: HttpRequest, attachment_uuid: uuid.UUID) -> HttpResponse:
    """Downloads an attachment

    Params:
        attachment_uuid: UUID of the attachment to download.
    """
    attachment = get_object_or_404(Attachment, uuid=attachment_uuid)
    return HttpResponse(
        attachment.content,
        content_type=attachment.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={attachment.filename}",
        },
    )
