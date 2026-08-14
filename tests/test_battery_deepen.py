"""Chip href sanitization, HTML escaping, query budgets, and filter fallbacks."""

from __future__ import annotations

from django.db import connection
from django.template import Context, Template
from django.test import SimpleTestCase, TestCase, override_settings
from django.test.utils import CaptureQueriesContext

from hashtag.filtering import filter_queryset_by_tag
from hashtag.models import MyTag
from hashtag.templatetags.hashtag_tags import _safe_href
from tests.models import ChipLabel, ChipTarget


class Tag:
    def __init__(self, name, slug, url=None):
        self.name = name
        self.slug = slug
        self._url = url

    def get_absolute_url(self):
        if self._url is None:
            from django.urls import NoReverseMatch

            raise NoReverseMatch("no route")
        return self._url


def render(arg, **ctx):
    template = Template(
        "{% load hashtag_tags %}{% hashtag_chips " + arg + " %}"
    )
    return template.render(Context(ctx))


class SafeHrefTests(SimpleTestCase):
    """Reject dangerous schemes and protocol-relative / backslash forms."""

    def test_rejects_vbscript_scheme(self):
        self.assertEqual(_safe_href("vbscript:msgbox(1)"), "")
        html = render(
            "tags",
            tags=[Tag("VB", "vb", url="vbscript:msgbox(1)")],
        )
        self.assertNotIn("vbscript:", html)
        self.assertNotIn("<a ", html)

    def test_rejects_protocol_relative_url(self):
        self.assertEqual(_safe_href("//evil.example/x"), "")
        html = render(
            "tags",
            tags=[Tag("Evil", "evil", url="//evil.example/x")],
        )
        self.assertNotIn("//evil", html)
        self.assertNotIn("<a ", html)

    def test_rejects_backslash_protocol_relative_forms(self):
        for href in (
            r"\\evil.example/x",
            r"/\evil.example/x",
            r"\\\evil.example/x",
        ):
            with self.subTest(href=repr(href)):
                self.assertEqual(_safe_href(href), "")
                html = render("tags", tags=[Tag("Evil", "evil", url=href)])
                self.assertNotIn("evil.example", html)
                self.assertNotIn("<a ", html)

    def test_rejects_leading_whitespace_javascript(self):
        for href in (
            " javascript:alert(1)",
            "\tjavascript:alert(1)",
            "\njavascript:alert(1)",
            "\xa0javascript:alert(1)",
        ):
            with self.subTest(href=repr(href)):
                self.assertEqual(_safe_href(href), "")
                html = render("tags", tags=[Tag("XSS", "xss", url=href)])
                self.assertNotIn("javascript:", html)
                self.assertNotIn("<a ", html)

    def test_javascript_scheme_still_rejected(self):
        self.assertEqual(_safe_href("javascript:alert(1)"), "")
        html = render(
            "tags",
            tags=[Tag("XSS", "xss", url="javascript:alert(1)")],
        )
        self.assertNotIn("javascript:", html)
        self.assertNotIn("<a ", html)


class ChipEscapeTests(SimpleTestCase):
    """Quotes and angle brackets in chip names are HTML-escaped."""

    def test_quotes_and_brackets_escaped_in_output(self):
        html = render(
            "tags linkable=False",
            tags=[Tag("a\"b'c<>d", "nasty")],
        )
        self.assertNotIn('a"b', html)
        self.assertNotIn("<d", html)
        self.assertNotIn(">d", html)
        self.assertIn("&lt;", html)
        self.assertIn("&gt;", html)
        self.assertTrue("&quot;" in html or "&#x27;" in html or "&#39;" in html)


class PlainStringChipsQueryBudgetTests(TestCase):
    """Plain string tags render with zero ORM queries."""

    def test_plain_string_tags_issue_zero_queries(self):
        with CaptureQueriesContext(connection) as ctx:
            html = render(
                'tags linkable=False prefix="#"',
                tags=["calm", "quiet", "spa"],
            )
        self.assertEqual(len(ctx.captured_queries), 0, ctx.captured_queries)
        self.assertIn("#calm", html)
        self.assertIn("#quiet", html)
        self.assertIn("#spa", html)


class FilterDistinctTests(TestCase):
    """Duplicate M2M joins collapse to distinct size."""

    def test_duplicate_label_joins_return_distinct_size(self):
        target = ChipTarget.objects.create(name="room-1")
        other = ChipTarget.objects.create(name="room-2")
        label_a = ChipLabel.objects.create(slug="spa")
        label_b = ChipLabel.objects.create(slug="spa")
        label_a.targets.add(target)
        label_b.targets.add(target)
        ChipLabel.objects.create(slug="pool").targets.add(other)

        inflated = ChipTarget.objects.filter(labels__slug="spa")
        self.assertEqual(inflated.count(), 2)

        filtered = filter_queryset_by_tag(
            ChipTarget.objects.all(), "spa", lookup="labels__slug"
        )
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(
            list(filtered.values_list("pk", flat=True)), [target.pk]
        )


class TagUrlDisabledFilterFallbackTests(TestCase):
    """When HASHTAG_TAG_URL_NAME is blank, chips use filter_url only."""

    @override_settings(HASHTAG_TAG_URL_NAME="")
    def test_chips_use_filter_url_when_canonical_disabled(self):
        tag = MyTag(name="Spa", slug="spa")
        html = render(
            'tags filter_url="/reviews/" filter_param="tag"',
            tags=[tag],
        )
        self.assertIn('href="/reviews/?tag=spa"', html)
        self.assertNotIn("/tag/spa/", html)

    @override_settings(HASHTAG_TAG_URL_NAME="")
    def test_chips_span_without_filter_url_when_canonical_disabled(self):
        tag = MyTag(name="Spa", slug="spa")
        html = render("tags", tags=[tag])
        self.assertNotIn("<a ", html)
        self.assertNotIn("/tag/spa/", html)
        self.assertIn("hashtag-chip", html)
