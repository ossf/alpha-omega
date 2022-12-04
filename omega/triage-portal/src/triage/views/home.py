from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from triage.models import Case, Finding, ToolDefect


@login_required
def home(request: HttpRequest) -> HttpResponse:
    finding_last_updated = Finding.objects.all().order_by("-updated_at").first().created_at
    case_last_updated = Case.objects.all().order_by("-updated_at").first().created_at
    my_work = {
        "num_cases": Case.objects.filter(assigned_to=request.user).count(),
        "num_findings": Finding.objects.filter(assigned_to=request.user).count(),
        "num_tool_defects": ToolDefect.objects.filter(assigned_to=request.user).count(),
    }
    metrics = {
        "num_findings": Finding.objects.count(),
        "num_active_findings": Finding.active_findings.count(),
        "num_new_findings": Finding.active_findings.filter(
            created_at__gt=timezone.now() - timedelta(days=7)
        ).count(),
    }
    context = {
        "finding_last_updated": finding_last_updated,
        "case_last_updated": case_last_updated,
        "my_work": my_work,
        "user": request.user,
        "metrics": metrics,
        "last_week": timezone.now() - timedelta(days=7),
    }
    return render(request, "triage/home.html", context)
