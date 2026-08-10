django-hashtag changelog
========================

.. towncrier release notes start

hashtag 0.4.2 (2026-08-10)
==========================

Features
--------

- Add ``hashtag.filtering`` helpers (``filter_queryset_by_tag``, ``active_tag_slug``) to share tag list filtering across views without referencing a consumer model.
- Add the ``hashtag_chips`` inclusion tag to render a tag collection as themeable, accessible chips, with optional in-context filter links and a shared base stylesheet.
- Make ``MyTag.get_absolute_url()`` configurable via the ``HASHTAG_TAG_URL_NAME`` setting (default ``tagged``; set to ``""`` to disable), so sites can use tags purely as an in-context ``?tag=`` filter.
