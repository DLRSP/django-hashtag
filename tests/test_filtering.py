"""Tests for the agnostic tag-filter helpers."""

from django.test import RequestFactory, SimpleTestCase

from hashtag.filtering import active_tag_slug, filter_queryset_by_tag


class FakeQuerySet:
    """Minimal queryset stub recording filter/distinct calls."""

    def __init__(self):
        self.calls = []

    def filter(self, **kwargs):
        self.calls.append(("filter", kwargs))
        return self

    def distinct(self):
        self.calls.append(("distinct", {}))
        return self


class FilterQuerysetByTagTest(SimpleTestCase):
    def test_filters_with_default_lookup_and_distinct(self):
        qs = FakeQuerySet()
        out = filter_queryset_by_tag(qs, "calm")
        self.assertIs(out, qs)
        self.assertEqual(
            qs.calls, [("filter", {"tags__slug": "calm"}), ("distinct", {})]
        )

    def test_custom_lookup(self):
        qs = FakeQuerySet()
        filter_queryset_by_tag(qs, "calm", lookup="labels__slug")
        self.assertEqual(qs.calls[0], ("filter", {"labels__slug": "calm"}))

    def test_empty_slug_returns_queryset_unchanged(self):
        qs = FakeQuerySet()
        out = filter_queryset_by_tag(qs, "")
        self.assertIs(out, qs)
        self.assertEqual(qs.calls, [])


class ActiveTagSlugTest(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_reads_tag_param(self):
        request = self.factory.get("/reviews/", {"tag": "spa"})
        self.assertEqual(active_tag_slug(request), "spa")

    def test_custom_param(self):
        request = self.factory.get("/reviews/", {"label": "spa"})
        self.assertEqual(active_tag_slug(request, param="label"), "spa")

    def test_missing_returns_empty_string(self):
        request = self.factory.get("/reviews/")
        self.assertEqual(active_tag_slug(request), "")


class ActiveSlugFilterIntegrationTest(SimpleTestCase):
    """Wire active_tag_slug into filter_queryset_by_tag the way list views do."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_request_slug_filters_queryset(self):
        request = self.factory.get("/reviews/", {"tag": "spa"})
        slug = active_tag_slug(request)
        qs = FakeQuerySet()
        out = filter_queryset_by_tag(qs, slug)
        self.assertIs(out, qs)
        self.assertEqual(
            qs.calls, [("filter", {"tags__slug": "spa"}), ("distinct", {})]
        )

    def test_missing_slug_leaves_queryset_unfiltered(self):
        request = self.factory.get("/reviews/")
        slug = active_tag_slug(request)
        qs = FakeQuerySet()
        filter_queryset_by_tag(qs, slug)
        self.assertEqual(qs.calls, [])
