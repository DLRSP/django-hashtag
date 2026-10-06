django-hashtag changelog
========================

.. towncrier release notes start

hashtag 0.4.7 (2026-10-06)
==========================

No significant changes.


hashtag 0.4.6 (2026-08-27)
==========================

No significant changes.


hashtag 0.4.5 (2026-08-14)
==========================

Bug Fixes
---------

- Make ``last_used`` default/sentinel respect ``USE_TZ``; reject backslash protocol-relative chip hrefs.


hashtag 0.4.4 (2026-08-14)
==========================

Bug Fixes
---------

- Sanitize chip hrefs to http(s)/relative only; make ``last_used`` fallback timezone-aware. (`#safe-chip-hrefs <https://github.com/DLRSP/django-hashtag/issues/safe-chip-hrefs>`_)


hashtag 0.4.3 (2026-08-14)
==========================

No significant changes.


hashtag 0.4.2 (2026-08-10)
==========================

Features
--------

- Add ``hashtag.filtering`` helpers (``filter_queryset_by_tag``, ``active_tag_slug``) to share tag list filtering across views without referencing a consumer model.
- Add the ``hashtag_chips`` inclusion tag to render a tag collection as themeable, accessible chips, with optional in-context filter links and a shared base stylesheet.
- Make ``MyTag.get_absolute_url()`` configurable via the ``HASHTAG_TAG_URL_NAME`` setting (default ``tagged``; set to ``""`` to disable), so sites can use tags purely as an in-context ``?tag=`` filter.
