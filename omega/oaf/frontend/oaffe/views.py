import zipfile
from packageurl import PackageURL

import logging
import io
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponseNotFound,
)
from oaffe.models import Assertion, Policy, Subject, PolicyEvaluationResult, AssertionGenerator
from oaffe.utils.policy import refresh_policies
from django.shortcuts import get_object_or_404


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
        subjects = Subject.objects.filter(identifier__icontains=query)
        c = {"subjects": subjects}
        return render(request, "search.html", c)
    else:
        return HttpResponseRedirect("/")


def refresh(request: HttpRequest) -> HttpResponse:
    refresh_policies()
    return HttpResponseRedirect("/")


def download_assertion(request: HttpRequest, assertion_uuid: str) -> HttpResponse:
    """
    Downloads a specific assertion (by UUID).
    """
    assertion = Assertion.objects.get(uuid=assertion_uuid)
    response = HttpResponse(json.dumps(assertion.content, indent=2), content_type="application/json")
    response["Content-Disposition"] = f'attachment; filename="oaf-{assertion_uuid}.json"'
    return response


def download_assertions(request: HttpRequest) -> HttpResponse:
    """Downloads all assertions as a zip file for the given subject."""
    subject_uuid = request.GET.get("subject_uuid")
    if not subject_uuid:
        return HttpResponseBadRequest("Missing subject uuid.")

    assertions = Assertion.objects.filter(subject__uuid=subject_uuid)
    if assertions.exists():
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
            for assertion in assertions:
                content = json.dumps(assertion.content, indent=2)
                zf.writestr(f"{assertion.uuid}.json", content)

        response = HttpResponse(buffer.getvalue(), content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="oaf-{subject_uuid}.zip"'
        return response
    else:
        return HttpResponseNotFound()


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
    subject_uuid = request.GET.get("subject_uuid")
    if subject_uuid:
        subject = get_object_or_404(Subject, pk=subject_uuid)
        assertions = Assertion.objects.filter(subject=subject)
        policies = PolicyEvaluationResult.objects.filter(subject=subject)

        other_subjects = []

        if subject.subject_type == Subject.SUBJECT_TYPE_PACKAGE_URL:
            purl = PackageURL.from_string(subject.identifier).to_dict()
            purl["version"] = None
            purl = PackageURL(**purl)

            related_subjects = Subject.objects.filter(
                subject_type=Subject.SUBJECT_TYPE_PACKAGE_URL,
                identifier__startswith=str(purl),
            ).exclude(identifier=subject.identifier)

        c = {
            "subject": subject,
            "assertions": assertions,
            "policies": policies,
            "related_subjects": sorted(related_subjects, key=lambda x: x.identifier),
        }
        return render(request, "view.html", c)

    else:
        return HttpResponseRedirect("/")


@csrf_exempt
def api_add_assertion(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.POST.get("assertion"))
    except:
        return HttpResponseBadRequest("Invalid assertion.")

    # Extract generator
    generator_name = data.get("predicate", {}).get("generator", {}).get("name") or ""
    generator_version = data.get("predicate", {}).get("generator", {}).get("version") or ""
    generator, _ = AssertionGenerator.objects.get_or_create(name=generator_name, version=generator_version)

    # Extract subject
    subject_type = data.get("subject", {}).get("type") or ""
    if subject_type == Subject.SUBJECT_TYPE_PACKAGE_URL:
        subject_identifier = data.get("subject", {}).get("purl")
    elif subject_type == Subject.SUBJECT_TYPE_GITHUB_URL:
        subject_identifier = data.get("subject", {}).get("github_url")
    else:
        return HttpResponseBadRequest("Invalid subject.")
    subject, _ = Subject.objects.get_or_create(subject_type=subject_type, identifier=subject_identifier)

    # Extract created date
    created_date = data.get("predicate", {}).get("operational", {}).get("timestamp")

    assertion = Assertion()
    assertion.generator = generator
    assertion.subject = subject
    assertion.content = data
    assertion.created_date = created_date
    assertion.save()

    refresh_policies(subject)

    return JsonResponse({"success": True})


def api_get_assertions_by_subject(request: HttpRequest) -> JsonResponse:
    """Retrieves all assertions for a specific subject."""
    subject = request.GET.get("subject")
    logging.debug("Retrieving assertions for subject[%s]", subject)

    if subject and subject.startswith("pkg:"):
        subject_obj = Subject.objects.filter(
            subject_type=Subject.SUBJECT_TYPE_PACKAGE_URL, identifier=subject
        ).first()
        if subject_obj:
            assertions = Assertion.objects.filter(subject=subject_obj).values()
            return JsonResponse(list(assertions), safe=False)
        else:
            return HttpResponseNotFound("No subject found.")
    else:
        return HttpResponseBadRequest("Invalid subject.")


def api_get_policies_by_subject(request: HttpRequest) -> JsonResponse:
    """Retrieve policies based on a provided subject."""
    subject = request.GET.get("subject")
    logging.debug("Retrieving assertions for subject[%s]", subject)

    if subject and subject.startswith("pkg:"):
        subject_obj = Subject.objects.filter(
            subject_type=Subject.SUBJECT_TYPE_PACKAGE_URL, identifier=subject
        ).first()
        if subject_obj:
            policies = Policy.objects.filter(subject=subject_obj).values()
            return JsonResponse(list(policies), safe=False)
        else:
            return HttpResponseNotFound("No subject found.")
    else:
        return HttpResponseBadRequest("Invalid subject.")
