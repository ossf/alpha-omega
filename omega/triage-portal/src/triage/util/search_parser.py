import datetime
import logging

import django.db.models.base
import pyparsing as pp
from django.db.models import Model, Q
from django.utils import timezone

from triage.models import Finding, WikiArticle, WorkItemState

logger = logging.getLogger(__name__)


def parse_query_to_Q(model: Model, query: str) -> Q:
    """
    Parse a query string into a Q object.
    """

    # Define the grammar
    assigned_to_clause = pp.Group(
        pp.Keyword("assigned_to").suppress()
        + pp.Literal(":").suppress()
        + pp.Word(pp.alphanums).setResultsName("username")
    ).setResultsName("assigned_to")

    priority_clause = pp.Group(
        pp.Keyword("priority").suppress()
        + pp.Literal(":").suppress()
        + pp.one_of(["<", ">", "<=", ">=", "==", "!="]).setResultsName("op")
        + pp.Word(pp.nums).setResultsName("value")
    ).setResultsName("priority")

    severity_clause = pp.Group(
        pp.Keyword("severity").suppress()
        + pp.Literal(":").suppress()
        + pp.delimited_list(
            pp.one_of(
                [
                    "critical",
                    "very high",
                    "vh",
                    "veryhigh",
                    "high",
                    "h",
                    "medium",
                    "m",
                    "low",
                    "very low",
                    "very_low",
                    "verylow",
                    "vl",
                    "informational",
                    "unknown",
                ]
            )
        )
    ).setResultsName("severity")

    updated_dt_clause = pp.Group(
        pp.Keyword("updated").suppress()
        + pp.Literal(":").suppress()
        + pp.one_of(["<", ">", "<=", ">=", "==", "!="]).setResultsName("op")
        + pp.pyparsing_common.iso8601_date("datetime")
    ).setResultsName("updated_dt")

    created_dt_clause = pp.Group(
        pp.Keyword("created").suppress()
        + pp.Literal(":").suppress()
        + pp.one_of(["<", ">", "<=", ">=", "==", "!="]).setResultsName("op")
        + (
            pp.pyparsing_common.iso8601_date("datetime")
            ^ (
                pp.one_of(["@today"]).setResultsName("anchor")
                + pp.one_of(["+", "-"]).setResultsName("anchor_op")
                + pp.Word(pp.nums).setResultsName("anchor_value")
            )
        )
    ).setResultsName("created_dt")

    state_clause = pp.Group(
        pp.Keyword("state").suppress()
        + pp.Literal(":").suppress()
        + pp.delimited_list(
            pp.one_of(
                [str(c[0]) for c in WorkItemState.choices]
                + [str(c[1]) for c in WorkItemState.choices],
                caseless=True,
            )
        ).setResultsName("states")
    ).setResultsName("state")

    purl_clause = pp.Group(
        pp.Keyword("purl").suppress()
        + pp.Literal(":").suppress()
        + pp.Word(pp.alphanums + ":@/?=-.").setResultsName("purl")
    ).setResultsName("purl")

    other_clause = pp.Word(pp.printables).setResultsName("text_search")

    available_attributes = [
        getattr(model, key).field.name
        for key in dir(model)
        if isinstance(getattr(model, key), django.db.models.query_utils.DeferredAttribute)
    ]

    parser_elements = []
    if "assigned_to" in available_attributes:
        parser_elements.append(assigned_to_clause)
    if "severity_level" in available_attributes:
        parser_elements.append(severity_clause)
    if "created_at" in available_attributes:
        parser_elements.append(created_dt_clause)
    if "updated_at" in available_attributes:
        parser_elements.append(updated_dt_clause)
    if "priority" in available_attributes:
        parser_elements.append(priority_clause)
    if "state" in available_attributes:
        parser_elements.append(state_clause)
    if "package_url" in available_attributes:
        parser_elements.append(purl_clause)
    if model == Finding:  # Special case for foreign key
        parser_elements.append(purl_clause)

    parser_elements.append(other_clause)
    parser_elements = list(dict.fromkeys(parser_elements))  # Unique only

    clause = parser_elements[0]

    if len(parser_elements) > 1:
        for element in parser_elements[1:]:
            clause |= element

    full_clause = pp.OneOrMore(clause)

    # Parse the query
    try:
        results = full_clause.parse_string(query)
    except:
        logger.error("Failed to parse query: %s", query)
        return None

    # Assemble the Q object
    q = Q()
    if results.assigned_to:
        q = q & Q(assigned_to__username=results.assigned_to.username)

    if results.severity:
        severities = map(Finding.SeverityLevel.parse, results.severity.asList())
        q = q & Q(severity_level__in=list(severities))

    if results.state:
        states = map(WorkItemState.parse, results.state.asList())
        q = q & Q(state__in=list(states))

    # Handle updated:$op$date or updated:$op@today[+-]$num
    if results.updated_dt:
        if results.updated_dt.datetime:
            target = results.updated_dt.datetime
        elif results.updated_dt.anchor:
            if results.updated_dt.anchor == "@today":
                target = timezone.now()
                if results.updated_dt.anchor_op == "-":
                    target -= datetime.timedelta(days=int(results.updated_dt.anchor_value))
                elif results.updated_dt.anchor_op == "+":
                    target += datetime.timedelta(days=int(results.updated_dt.anchor_value))
            else:
                raise ValueError("Unknown anchor: %s" % results.updated_dt.anchor)
        else:
            raise ValueError("Unknown updated_dt: %s" % results.updated_dt)

        if results.updated_dt.op == "<":
            q = q & Q(updated_at__lt=target)
        elif results.updated_dt.op == ">":
            q = q & Q(updated_at__gt=target)
        elif results.updated_dt.op == "<=":
            q = q & Q(updated_at__lte=target)
        elif results.updated_dt.op == ">=":
            q = q & Q(updated_at__gte=target)
        elif results.updated_dt.op == "==":
            q = q & Q(updated_at__exact=target)
        elif results.updated_dt.op == "!=":
            q = q & ~Q(created_at__exact=target)
        else:
            logger.warning("Unknown updated_dt op: %s", results.updated_dt.op)

    if results.created_dt:
        if results.created_dt.datetime:
            target = results.created_dt.datetime
        elif results.created_dt.anchor:
            if results.created_dt.anchor == "@today":
                target = timezone.now()
                if results.created_dt.anchor_op == "-":
                    target -= datetime.timedelta(days=int(results.created_dt.anchor_value))
                elif results.created_dt.anchor_op == "+":
                    target += datetime.timedelta(days=int(results.created_dt.anchor_value))
            else:
                raise ValueError("Unknown anchor: %s" % results.created_dt.anchor)
        else:
            raise ValueError("Unknown created_dt: %s" % results.created_dt)

        if results.created_dt.op == "<":
            q = q & Q(created_at__lt=target)
        elif results.created_dt.op == ">":
            q = q & Q(created_at__gt=target)
        elif results.created_dt.op == "<=":
            q = q & Q(created_at__lte=target)
        elif results.created_dt.op == ">=":
            q = q & Q(created_at__gte=target)
        elif results.created_dt.op == "==":
            q = q & Q(created_at__exact=target)
        elif results.created_dt.op == "!=":
            q = q & ~Q(created_at__exact=target)
        else:
            logger.warning("Unknown created_dt op: %s", results.created_dt.op)

    if results.priority:
        if results.priority.op == "<":
            q = q & Q(priority__lt=results.priority.value)
        elif results.priority.op == ">":
            q = q & Q(priority__gt=results.priority.value)
        elif results.priority.op == "<=":
            q = q & Q(priority__lte=results.priority.value)
        elif results.priority.op == ">=":
            q = q & Q(priority__gte=results.priority.value)
        elif results.priority.op == "==":
            q = q & Q(priority__exact=results.priority.value)
        elif results.priority.op == "!=":
            q = q & ~Q(priority__exact=results.priority.value)
        else:
            logger.warning("Unknown priority op: %s", results.priority.op)

    if results.purl:
        if "project_version" in available_attributes:
            q = q & (
                Q(project_version__project__package_url=results.purl.purl)
                | Q(project_version__package_url=results.purl.purl)
            )
        if "package_url" in available_attributes:
            q = q & Q(package_url=results.purl.purl)

    # Handle full text search a little differently
    if results.text_search:
        text_qq = Q()
        if "project_version" in available_attributes:
            text_qq |= Q(project_version__project__name__icontains=results.text_search)
        if "title" in available_attributes:
            text_qq |= Q(title__icontains=results.text_search)
        if "description" in available_attributes:
            text_qq |= Q(description__icontains=results.text_search)

        if model == WikiArticle:  # @HACK: Special case for foreign key
            text_qq |= Q(current__content__icontains=results.text_search)

        q = q & text_qq

    logger.debug("Query: %s", q)
    return q
