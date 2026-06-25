# django-hashtag [![PyPi license](https://img.shields.io/pypi/l/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)

[![PyPi status](https://img.shields.io/pypi/status/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)
[![PyPi version](https://img.shields.io/pypi/v/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)
[![PyPi python version](https://img.shields.io/pypi/pyversions/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)
[![PyPi downloads](https://img.shields.io/pypi/dm/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)
[![PyPi downloads](https://img.shields.io/pypi/dw/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)
[![PyPi downloads](https://img.shields.io/pypi/dd/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)

## GitHub ![GitHub release](https://img.shields.io/github/tag/DLRSP/django-hashtag.svg) ![GitHub release](https://img.shields.io/github/release/DLRSP/django-hashtag.svg)

## Test [![codecov.io](https://codecov.io/github/DLRSP/django-hashtag/coverage.svg?branch=main)](https://codecov.io/github/DLRSP/django-hashtag?branch=main) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DLRSP/django-hashtag/main.svg)](https://results.pre-commit.ci/latest/github/DLRSP/django-hashtag/main) [![gitthub.com](https://github.com/DLRSP/django-hashtag/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-hashtag/actions/workflows/ci.yaml)

## Check Demo Project
* Check the demo repo on [GitHub](https://github.com/DLRSP/example/tree/django-hashtag)

## Requirements
-   Python 3.9, 3.10, 3.11, 3.12, 3.13, 3.14 supported.
-   Django 3.2, 4.2 and 5.2 supported.

We **highly recommend** and only officially support the latest patch release of each Python and Django series.

## Setup
1. Install from **pip**:
```shell
pip install django-hashtag
```

2. Modify `settings.py` by adding the app to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    "taggit",
    "hashtag",
    # ...
]
```

3. Execute Django's command `migrate` inside your project's root:
```sheel
python manage.py migrate
Running migrations:
  Applying hashtag.0001_initial... OK
  Applying hashtag.0002_alter_mytag_slug... OK
  Applying hashtag.0003_alter_mytag_last_used... OK
```

## Usage

`django-hashtag` provides the tag data model plus reusable, consumer-agnostic
helpers so every site renders and filters tags the same way without
re-implementing the markup or the queryset logic.

### Render tags as chips (`hashtag_chips`)

The `hashtag_chips` inclusion tag renders a tag collection as accessible chips.
It accepts model instances (exposing `name`/`slug`/`get_absolute_url`) or plain
strings.

```html
{% load hashtag_tags %}

{# Static, non-linkable chips (e.g. a homepage badge row) #}
{% hashtag_chips tags variant="home" linkable=False %}

{# In-context filter links: builds <filter_url>?<filter_param>=<slug> #}
{% hashtag_chips tags variant="review" filter_url=request.path filter_param="tag" %}

{# Custom href pattern with a {slug} placeholder #}
{% hashtag_chips tags href_pattern="/reviews/?tag={slug}" %}
```

Arguments:

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

Style the chips per site via CSS custom properties on the shared classes
(`hashtag-chip`, `hashtag-chip--<variant>`); a base stylesheet ships at
`hashtag/static/hashtag/hashtag-chips.css`.

### Filter a list by tag

`hashtag.filtering` shares the queryset filter and active-tag lookup used by
in-context list views, without referencing any consumer model:

```python
from hashtag.filtering import active_tag_slug, filter_queryset_by_tag

def review_list(request):
    slug = active_tag_slug(request)            # reads ?tag=<slug>
    reviews = filter_queryset_by_tag(Review.objects.all(), slug)
    # ...build your own context/template/pagination...
```

`filter_queryset_by_tag` accepts a `lookup` argument (default `"tags__slug"`)
for non-default relation paths; an empty slug returns the queryset unchanged.

### Optional canonical tag page (`HASHTAG_TAG_URL_NAME`)

`MyTag.get_absolute_url()` is configurable via `HASHTAG_TAG_URL_NAME`, which
defaults to `"tagged"` for backward compatibility. Set it to `""` to disable
canonical tag pages:

```python title="settings.py"
# Enable canonical per-tag URLs resolved with reverse(name, args=[slug]).
HASHTAG_TAG_URL_NAME = "tagged"

# Or disable canonical tag pages entirely (sites that surface tags only as an
# in-context ?tag= filter); get_absolute_url() then raises NoReverseMatch and
# hashtag_chips falls back to filter_url/href_pattern.
HASHTAG_TAG_URL_NAME = ""
```

## Run Example Project

```shell
git clone --depth=50 --branch=django-hashtag https://github.com/DLRSP/example.git DLRSP/example
cd DLRSP/example
python manage.py runserver
```

Now browser the app @ http://127.0.0.1:8000
