import zipfile
import io
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from oaffe.models import Assertion, Policy
from oaffe.utils.policy import refresh_policies
from oaffe.utils import normalize_subject


def home(request: HttpRequest) -> HttpResponse:
    """Home page view for the OAF UI."""
    return render(request, "home.html")


def api_get_assertion(request: HttpRequest, assertion_uuid: str) -> JsonResponse:
    assertion = Assertion.objects.get(uuid=assertion_uuid)
    return JsonResponse(
        {"uuid": assertion.uuid, "generator": assertion.generator, "content": assertion.content}
    )


def search_subjects(request: HttpRequest) -> HttpResponse:
    """Searches the database for subjects that match a given query.
    Searches are basic, case-insensitive 'contains'.
    """
    query = request.GET.get("q")
    if query:
        subjects = (
            Assertion.objects.filter(subject__icontains=query)
            .order_by("subject")
            .values_list("subject", flat=True)
            .distinct()
        )
    else:
        return HttpResponseRedirect("/")

    c = {"subjects": map(normalize_subject, subjects)}
    return render(request, "search.html", c)


def refresh(request: HttpRequest) -> HttpResponse:
    refresh_policies()
    return HttpResponseRedirect("/")


def download_assertion(request: HttpRequest, assertion_uuid: str) -> HttpResponse:
    assertion = Assertion.objects.get(uuid=assertion_uuid)
    response = HttpResponse(json.dumps(assertion.content, indent=2), content_type="application/json")
    response["Content-Disposition"] = f'attachment; filename="{assertion_uuid}.json"'
    return response


def download_assertions(request: HttpRequest) -> HttpResponse:
    """Downloads all assertions as a zip file for the given subject."""
    subject = request.GET.get("subject")
    if not subject:
        return HttpResponseBadRequest("Missing subject.")

    assertions = Assertion.objects.filter(subject=subject)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
        for assertion in assertions:
            content = json.dumps(assertion.content, indent=2)
            zf.writestr(f"{assertion.uuid}.json", content)

    response = HttpResponse(buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{subject}.zip"'
    return response


def policy_heapmap(request: HttpRequest) -> HttpResponse:
    policies = Policy.objects.all()
    subjects = set([p.subject for p in policies])
    result = {}
    for subject in subjects:
        if subject not in result:
            result[subject] = {}

        for policy in policies:
            if policy.subject == subject:
                result[subject][policy.policy] = policy.status

    c = {"result": result}

    return render(request, "heatmap.html", c)


def show_assertions(request: HttpRequest) -> HttpResponse:
    subject = request.GET.get("subject")
    if subject:
        assertions = Assertion.objects.filter(subject=subject)
        policies = Policy.objects.filter(subject=subject)
        distinct_subjects = (
            Assertion.objects.filter(subject__startswith=subject.split("@")[0] + "@")
            .values_list("subject", flat=True)
            .distinct()
        )
        versions = [(ds, ds.split("@")[1]) for ds in distinct_subjects]
    else:
        return HttpResponseRedirect("/")

    c = {
        "subject": normalize_subject(subject),
        "assertions": assertions,
        "policies": policies,
        "versions": sorted(versions, key=lambda x: x[1]),
    }
    return render(request, "view.html", c)


@csrf_exempt
def api_add_assertion(request: HttpRequest) -> JsonResponse:
    print(request.POST)

    assertion = json.loads(request.POST.get("assertion"))

    # Pull the generator out
    generator_str = assertion.get("predicate", {}).get("generator", {}).get("name") or "unknown"
    created_dt = assertion.get("predicate", {}).get("operational", {}).get("timestamp")

    # Pull the subject out
    subject = assertion.get("subject", {})
    if subject:
        subject_type = subject.get("type")
        if subject_type == "https://github.com/ossf/alpha-omega/subject/package_url/v0.1":
            purl = subject.get("purl")
            subject_str = f"{subject_type}:{purl}"
        elif subject_type == "https://github.com/ossf/alpha-omega/subject/github_url/v0.1":
            github_url = subject.get("github_url")
            subject_str = f"{subject_type}:{github_url}"
        else:
            return HttpResponseBadRequest("Invalid subject type.")
    else:
        return HttpResponseBadRequest("No subject provided.")

    ao = Assertion()

    ao.generator = generator_str
    ao.subject = subject_str
    ao.content = assertion
    ao.updated_dt = created_dt

    ao.save()

    refresh_policies(subject=subject_str)

    return JsonResponse({"success": True})
