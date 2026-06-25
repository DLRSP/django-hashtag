"""Agnostic tag-filter helpers for in-context list views.

The owning view keeps its own URL, template, pagination and context; these
helpers only encapsulate the queryset filter and the active-tag lookup so the
logic is shared instead of re-implemented per consumer. Nothing here references
a consumer model: the queryset and the relation lookup are inputs.
"""


def filter_queryset_by_tag(queryset, slug, lookup="tags__slug"):
    """Return ``queryset`` filtered to objects carrying the tag ``slug``.

    ``lookup`` is the ORM path to the tag slug (default suits taggit's
    ``tags`` manager). Empty ``slug`` returns the queryset unchanged.
    """
    if not slug:
        return queryset
    return queryset.filter(**{lookup: slug}).distinct()


def active_tag_slug(request, param="tag"):
    """Read the active tag slug from the request query string (``?tag=``)."""
    return request.GET.get(param) or ""
