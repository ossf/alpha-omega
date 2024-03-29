from core.settings import STATIC_ROOT
import os
from datetime import datetime, timezone
import markdown
import zipfile
from packageurl import PackageURL
import logging
import io
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponseNotFound,
)
from oaffe.models import (
    Assertion,
    Policy,
    Subject,
    PolicyEvaluationResult,
    AssertionGenerator,
    PolicyGroup,
    PackageRequest,
    PolicyEvaluationQueue,
)
from oaffe.utils.policy import refresh_policies
from oaffe.utils.dependencies import get_dependencies
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)


def home(request: HttpRequest) -> HttpResponse:
    """Home page view for the OAF UI."""
    return render(request, "home.html", {"page_title": "Assurance Assertions Home"})


def api_get_assertion(request: HttpRequest, assertion_uuid: str) -> JsonResponse:
    assertion = Assertion.objects.get(uuid=assertion_uuid)
    return JsonResponse(assertion.to_dict())


def clamp(value, min_value, max_value):
    """Clamp a value between a minimum and maximum value."""
    return max(min_value, min(float(value), max_value))


def search_subjects(request: HttpRequest) -> HttpResponse:
    """Searches the database for subjects that match a given query.
    Searches are basic, case-insensitive 'contains'.
    """
    query = request.GET.get("q")
    if query:
        page_size = clamp(request.GET.get("page_size", 20), 10, 500)
        page = clamp(request.GET.get("page", 1), 1, 1000)

        subjects = Subject.objects.filter(identifier__icontains=query)

        subject_map = {}
        for subject in subjects:
            cur_version = None

            if subject.subject_type == Subject.SUBJECT_TYPE_PACKAGE_URL:
                top_identifier = PackageURL.from_string(subject.identifier).to_dict()
                cur_version = top_identifier["version"]
                top_identifier["version"] = None
                top_identifier = PackageURL(**top_identifier)
            elif subject.subject_type == Subject.SUBJECT_TYPE_GITHUB_URL:
                top_identifier = subject.identifier
            else:
                raise ValueError("Unexpected subject type.")

            top_identifier = str(top_identifier)

            if top_identifier not in subject_map:
                subject_map[top_identifier] = []

            if cur_version:
                subject_map[top_identifier].append({"uuid": str(subject.uuid), "version": cur_version})

        subject_map = [(k, v) for k, v in subject_map.items()]
        paginator = Paginator(subject_map, page_size)

        query_string = request.GET.copy()
        if "page" in query_string:
            query_string.pop("page", None)

        context = {
            "query": query,
            "subjects": paginator.get_page(page),
            "params": query_string.urlencode(),
        }
        return render(request, "search.html", context)
    else:
        return HttpResponseRedirect("/")


def refresh(request: HttpRequest) -> HttpResponse:
    refresh_policies()
    return HttpResponseRedirect("/")


def data_dump(request: HttpRequest) -> HttpResponse:
    dump_path = STATIC_ROOT
    if not dump_path:
        dump_path = os.path.abspath(os.path.join(__file__, "../../oaffe/static/oaffe"))
    filename = os.path.join(dump_path, "policy_evaluations.csv")

    if os.path.isfile(filename):
        stat_result = os.stat(filename)
        _date = datetime.fromtimestamp(stat_result.st_mtime, tz=timezone.utc)
        c = {"generated_date": _date}
    else:
        c = {}

    return render(request, "data_dump.html", c)


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


from django.db.models import Count, Q


def policy_summary(request: HttpRequest) -> HttpResponse:
    policies = Policy.objects.all().annotate(
        is_passed=Count("pk", filter=Q(policyevaluationresult__status="PA")),
        is_failed=Count("pk", filter=Q(policyevaluationresult__status="FA")),
    )
    c = {
        'policies': policies
    }

    return render(request, "policy_summary.html", c)

def policy_detail(request: HttpRequest) -> HttpResponse:
    policy_identifier = request.GET.get("policy_identifier")
    if not policy_identifier:
        return HttpResponseBadRequest("Missing policy identifier.")

    policy_filter = request.GET.get("policy_filter")
    if policy_filter and policy_filter not in PolicyEvaluationResult.Status.values:
        return HttpResponseBadRequest("Invalid policy evaluation filter status.")

    policy = Policy.objects.filter(identifier=policy_identifier).first()
    if not policy:
        return HttpResponseNotFound("Policy not found.")

    evaluation_results = policy.policyevaluationresult_set.all()
    if policy_filter:
        evaluation_results = evaluation_results.filter(status=policy_filter)

    c = {
        'policy': policy,
        'evaluation_results': evaluation_results,
        'policy_filter': policy_filter,
    }

    return render(request, "policy_detail.html", c)


def calculate_dependency_PERs(dependency_map: dict[str, list[str]]) -> list:
    """Calculates PolicyExecutionResults for each dependency provided."""
    results = {"direct": {}, "indirect": {}, "policies": []}

    if not dependency_map:
        return results

    policy_map = {}
    index = 0

    # Gather up all of the policies
    for policy in Policy.objects.all():
        if policy not in policy_map:
            policy_map[policy] = index
            index += 1
    results["policies"] = policy_map.keys()

    # Replace all subjects with objects when known
    for _type in ["direct", "indirect"]:
        subjects = set(dependency_map.get(_type, []))
        subject_objs = Subject.objects.filter(identifier__in=subjects)
        for subject_obj in subject_objs:
            subjects.discard(subject_obj.identifier)
        subjects = subjects.union(subject_objs)
        dependency_map[_type] = subjects

    # Generate the map structure
    for _type in ["direct", "indirect"]:
        subjects = dependency_map.get(_type, [])
        for subject in subjects:
            results[_type][subject] = [None] * index

        # Now populate the grid where we have data
        for per in PolicyEvaluationResult.objects.filter(subject__identifier__in=subjects):
            subject = per.subject
            results[_type][subject][policy_map[per.policy]] = per

    return results


def show_assertions(request: HttpRequest) -> HttpResponse:
    subject_uuid = request.GET.get("subject_uuid")
    if subject_uuid:
        subject = get_object_or_404(Subject, pk=subject_uuid)
        assertions = Assertion.objects.filter(subject=subject)
        dependencies = {}

        policy_evaluation_results = PolicyEvaluationResult.objects.filter(subject=subject)

        policy_group_uuid = request.GET.get("policy_group_uuid")
        if policy_group_uuid:
            policy_group = get_object_or_404(PolicyGroup, pk=policy_group_uuid)
            policy_evaluation_results = policy_evaluation_results.filter(
                policy__in=policy_group.policies.all()
            )

        other_subjects = []
        dep_pers = {}
        # policy_keys = []

        if subject.subject_type == Subject.SUBJECT_TYPE_PACKAGE_URL:
            purl = PackageURL.from_string(subject.identifier).to_dict()
            purl["version"] = None
            purl = PackageURL(**purl)

            related_subjects = Subject.objects.filter(
                subject_type=Subject.SUBJECT_TYPE_PACKAGE_URL,
                identifier__startswith=str(purl),
            ).exclude(identifier=subject.identifier)

            dependencies = get_dependencies(PackageURL.from_string(subject.identifier))
            if dependencies is not None:
                dep_pers = calculate_dependency_PERs(dependencies)

        c = {
            "subject": subject,
            "assertions": assertions,
            "dep_pers": dep_pers,
            "policy_evaluation_results": policy_evaluation_results,
            "related_subjects": sorted(subject.get_versions(), key=lambda x: x.identifier),
            "policy_group_uuid": policy_group_uuid,
            "policy_groups": PolicyGroup.objects.all(),
        }
        return render(request, "view.html", c)

    else:
        return HttpResponseRedirect("/")


def package_request(request: HttpRequest) -> HttpResponse:
    """Handles interaction with the 'request a package' function."""
    if request.method == "POST":
        content = request.POST.get("package_list")
        if content:
            for _line in content.splitlines():
                line = _line.strip()
                if not line or len(line) > 500:
                    continue
                PackageRequest(package=line).save()
            return HttpResponseRedirect("/package_request?action=complete")
    else:
        return render(request, "package_request.html", {"complete": request.GET.get("action") == "complete"})


def api_get_help(request: HttpRequest) -> JsonResponse:
    """Retrieve help text for a given policy or assertion generator."""
    _type = request.GET.get("type")
    if _type == "policy":
        policy_uuid = request.GET.get("policy_uuid")
        policy = get_object_or_404(Policy, pk=policy_uuid)
        return HttpResponse(markdown.markdown(policy.help_text or ""))

    elif _type == "assertion_generator":
        assertion_generator_uuid = request.GET.get("assertion_generator_uuid")
        generator = get_object_or_404(AssertionGenerator, pk=assertion_generator_uuid)
        return HttpResponse(markdown.markdown(generator.help_text or ""))

    return HttpResponseBadRequest("Help not found.")


@csrf_exempt
def api_add_assertion(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.POST.get("assertion"))
    except:
        return HttpResponseBadRequest("Invalid assertion.")

    # Extract generator
    generator_name = data.get("predicate", {}).get("generator", {}).get("name") or ""
    generator_version = data.get("predicate", {}).get("generator", {}).get("version") or ""
    generator, _ = AssertionGenerator.objects.get_or_create(
        name=generator_name, version=generator_version, defaults={"name_readable": generator_name}
    )

    # Extract subject
    subject_type = data.get("subject", {}).get("type") or ""
    if subject_type == Subject.SUBJECT_TYPE_PACKAGE_URL:
        subject_identifier = data.get("subject", {}).get("purl")
    elif subject_type == Subject.SUBJECT_TYPE_GITHUB_URL:
        subject_identifier = data.get("subject", {}).get("github_url")
    else:
        return HttpResponseBadRequest("Invalid subject.")
    subject, _ = Subject.objects.get_or_create(subject_type=subject_type, identifier=subject_identifier)

    logger.debug("Adding assertion, subject=%s", subject)

    # Extract created date
    created_date = data.get("predicate", {}).get("operational", {}).get("timestamp")

    try:
        assertion, _ = Assertion.objects.get_or_create(
            generator=generator, subject=subject, content=data, created_date=created_date
        )
    except Assertion.MultipleObjectsReturned:
        logger.debug("Multiple assertions were found, deleting all but one.")

        Assertion.objects.filter(
            generator=generator, subject=subject, content=data, created_date=created_date
        ).delete()

        assertion = Assertion(generator=generator, subject=subject, content=data, created_date=created_date)
        assertion.save()

    # Add subject to the evaluation queue
    logger.debug("Adding subject[%s] to the evaluation queue.", subject)
    PolicyEvaluationQueue.objects.get_or_create(subject=subject)

    return JsonResponse({"success": True})


def _get_subject_from_request(request: HttpRequest) -> Subject:
    """Retrieve a subject from a request."""
    if "subject_uuid" in request.GET:
        subject_uuid = request.GET.get("subject_uuid")
        logger.debug("Retrieving assertions for subject[%s]", subject_uuid)
        subject = get_object_or_404(Subject, uuid=subject_uuid)
    elif "subject_identifier" in request.GET:
        subject_identifier = request.GET.get("subject_identifier")
        logger.debug("Retrieving assertions for subject[%s]", subject_identifier)
        subject = get_object_or_404(Subject, identifier=subject_identifier)
    else:
        raise ValueError("Invalid subject.")

    if not subject:
        raise Http404("No subject found.")

    return subject


def api_get_assertions(request: HttpRequest) -> JsonResponse:
    """Retrieve assertions based on API parameters."""
    subject = _get_subject_from_request(request)
    assertions = Assertion.objects.filter(subject=subject)
    return JsonResponse(list(a.to_dict() for a in assertions), safe=False, json_dumps_params={"indent": 2})


def api_get_policy_evaluation_results(request: HttpRequest) -> JsonResponse:
    """Retrieve policy evaluations based on API parameters."""
    subject = _get_subject_from_request(request)

    results = PolicyEvaluationResult.objects.filter(subject=subject)

    # Further filter by policy group
    if "policy_group_uuid" in request.GET:
        policy_group = get_object_or_404(PolicyGroup, uuid=request.GET.get("policy_group_uuid"))
        results = results.filter(policy__in=policy_group.policies.all())

    return JsonResponse(list(r.to_dict() for r in results), safe=False, json_dumps_params={"indent": 2})
