Django application that provides hashtag/tag functionality on top of
[django-taggit](https://github.com/jazzband/django-taggit), with reusable,
consumer-agnostic helpers to render and filter tags consistently across sites.

---

## Requirements

These packages are required:

* Python (3.9, 3.10, 3.11, 3.12, 3.13, 3.14)
* Django (3.2, 4.2, 5.2)

We **highly recommend** and only officially support the latest patch release of
each Python and Django series.

## Installation

1. Install using `pip`:

    ``` shell
    pip install django-hashtag
    ```

2. Add `taggit` and `hashtag` to your `INSTALLED_APPS`:

    ``` python title="settings.py"
    INSTALLED_APPS = [
        # ...other apps
        "taggit",
        "hashtag",
    ]
    ```

3. Run migrations:

    ``` shell
    python manage.py migrate
    ```

## What you get

* A tag data model (`MyTag`, `MyTagGroup`, `MyTaggedItem`).
* A reusable `hashtag_chips` template tag to render tags as themeable chips.
* `hashtag.filtering` helpers to filter list views by the active tag.
* An opt-in canonical tag URL via the `HASHTAG_TAG_URL_NAME` setting.

See the [Templates](tutorial/templates.md) guide for usage.

## Example

* Check the demo repo on [GitHub][github-demo].

## Development

See the [Contribution guidelines](community/contributing.md) for how to clone
the repository, run the test suite and contribute changes back to
django-hashtag.

[github-demo]: https://github.com/DLRSP/example/tree/django-hashtag
