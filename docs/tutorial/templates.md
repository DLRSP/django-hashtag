# Templates and helpers

`django-hashtag` ships reusable, consumer-agnostic helpers so every site renders
and filters tags the same way, without re-implementing markup or queryset logic.

## Render tags as chips: `hashtag_chips`

The `hashtag_chips` inclusion tag renders a tag collection as accessible chips.
It accepts model instances (exposing `name`/`slug`/`get_absolute_url`) or plain
strings.

``` html
{% load hashtag_tags %}

{# Static, non-linkable chips (e.g. a homepage badge row) #}
{% hashtag_chips tags variant="home" linkable=False %}

{# In-context filter links: builds <filter_url>?<filter_param>=<slug> #}
{% hashtag_chips tags variant="review" filter_url=request.path filter_param="tag" %}

{# Custom href pattern with a {slug} placeholder #}
{% hashtag_chips tags href_pattern="/reviews/?tag={slug}" %}
```

### Arguments

| Argument | Default | Description |
|---|---|---|
| `tags` | — | Iterable of tag instances or strings. |
| `variant` | `""` | Theme modifier; adds `hashtag-chips--<variant>` / `hashtag-chip--<variant>`. |
| `linkable` | `True` | When `False`, render `<span>` chips instead of links. |
| `prefix` | `"#"` | Text prefix shown before each tag name. |
| `filter_url` | `""` | Build an in-context filter link `<filter_url>?<filter_param>=<slug>`. |
| `filter_param` | `"tag"` | Query parameter used with `filter_url`. |
| `href_pattern` | `""` | Link template with a `{slug}` placeholder. |
| `link_class` | `""` | Extra CSS class added to each link. |
| `channel` | `"tag"` | Value for the `data-channel` attribute (analytics hook). |
| `placement` | `""` | Value for the `data-placement` attribute (analytics hook). |
| `label` | `""` | Accessible `aria-label` for the chip list. |

Href resolution order: `filter_url` -> `href_pattern` -> `get_absolute_url()`
(when reversible) -> none (renders a `<span>`).

### Theming

Style chips per site via CSS custom properties on the shared classes
(`hashtag-chip`, `hashtag-chip--<variant>`). A base stylesheet ships at
`hashtag/static/hashtag/hashtag-chips.css`. Load it (or your own theme) in your
template:

``` html
{% load static %}
<link rel="stylesheet" href="{% static 'hashtag/hashtag-chips.css' %}">
```

## Filter a list by tag

`hashtag.filtering` shares the queryset filter and active-tag lookup used by
in-context list views, without referencing any consumer model:

``` python
from hashtag.filtering import active_tag_slug, filter_queryset_by_tag

def review_list(request):
    slug = active_tag_slug(request)            # reads ?tag=<slug>
    reviews = filter_queryset_by_tag(Review.objects.all(), slug)
    # ...build your own context/template/pagination...
```

`filter_queryset_by_tag` accepts a `lookup` argument (default `"tags__slug"`)
for non-default relation paths; an empty slug returns the queryset unchanged.

## Optional canonical tag page: `HASHTAG_TAG_URL_NAME`

`MyTag.get_absolute_url()` is configurable via `HASHTAG_TAG_URL_NAME`, which
defaults to `"tagged"` for backward compatibility. Set it to `""` to disable
canonical tag pages:

``` python title="settings.py"
# Enable canonical per-tag URLs resolved with reverse(name, args=[slug]).
HASHTAG_TAG_URL_NAME = "tagged"

# Or disable canonical tag pages entirely (sites that surface tags only as an
# in-context ?tag= filter); get_absolute_url() then raises NoReverseMatch and
# hashtag_chips falls back to filter_url/href_pattern.
HASHTAG_TAG_URL_NAME = ""
```
