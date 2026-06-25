"""Reusable rendering helpers for tag collections."""

from django import template
from django.urls import NoReverseMatch

register = template.Library()


@register.inclusion_tag("hashtag/chips.html")
def hashtag_chips(
    tags,
    variant="",
    linkable=True,
    prefix="#",
    filter_url="",
    filter_param="tag",
    href_pattern="",
    link_class="",
    channel="tag",
    placement="",
    label="",
):
    """Render a tag collection as chips.

    ``tags`` accepts model instances (``name``/``slug``/``get_absolute_url``)
    or plain strings. Href resolution order: ``filter_url`` (builds an
    in-context filter link ``<filter_url>?<filter_param>=<slug>``) ->
    ``href_pattern`` (with a ``{slug}`` placeholder) -> ``get_absolute_url()``
    when reversible -> none. The base markup and class contract are shared
    across consumers; each site themes the chips via CSS variables on
    ``hashtag-chip``/``hashtag-chip--<variant>``.
    """
    items = []
    for tag in tags or []:
        name = getattr(tag, "name", None) or str(tag)
        slug = getattr(tag, "slug", "")
        href = ""
        if linkable:
            if filter_url and slug:
                separator = "&" if "?" in filter_url else "?"
                href = f"{filter_url}{separator}{filter_param}={slug}"
            elif href_pattern and slug:
                href = href_pattern.replace("{slug}", str(slug))
            else:
                getter = getattr(tag, "get_absolute_url", None)
                if callable(getter):
                    try:
                        href = getter()
                    except NoReverseMatch:
                        href = ""
        items.append({"name": name, "slug": slug, "href": href})
    return {
        "items": items,
        "variant": variant,
        "prefix": prefix,
        "link_class": link_class,
        "channel": channel,
        "placement": placement,
        "label": label,
    }
