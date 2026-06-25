"""Tests for the hashtag_chips inclusion tag."""

from django.template import Context, Template
from django.test import SimpleTestCase


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
    template = Template("{% load hashtag_tags %}{% hashtag_chips " + arg + " %}")
    return template.render(Context(ctx))


class HashtagChipsTest(SimpleTestCase):
    def test_renders_linkable_chips_with_href_pattern(self):
        html = render(
            'tags variant="review" href_pattern="/reviews/?tag={slug}"',
            tags=[Tag("Great Location", "great-location")],
        )
        self.assertIn('class="hashtag-chips hashtag-chips--review"', html)
        self.assertIn('href="/reviews/?tag=great-location"', html)
        self.assertIn("hashtag-chip--review", html)
        self.assertIn('rel="nofollow"', html)
        self.assertIn("#Great Location", html)

    def test_non_linkable_renders_span_without_prefix(self):
        html = render(
            'tags variant="home" linkable=False prefix=""',
            tags=[Tag("Sea View", "sea-view")],
        )
        self.assertNotIn("<a ", html)
        self.assertIn("hashtag-chip--home", html)
        self.assertIn(">Sea View<", html)

    def test_filter_url_builds_in_context_link(self):
        html = render(
            'tags variant="review" filter_url="/reviews/" filter_param="tag"',
            tags=[Tag("Sea View", "sea-view")],
        )
        self.assertIn('href="/reviews/?tag=sea-view"', html)

    def test_filter_url_appends_when_query_already_present(self):
        html = render(
            'tags filter_url="/reviews/?lang=it"',
            tags=[Tag("Spa", "spa")],
        )
        self.assertIn("lang=it", html)
        self.assertIn("tag=spa", html)
        self.assertNotIn("?tag=spa", html)

    def test_filter_url_takes_precedence_over_href_pattern(self):
        html = render(
            'tags filter_url="/reviews/" href_pattern="/other/?t={slug}"',
            tags=[Tag("Spa", "spa")],
        )
        self.assertIn('href="/reviews/?tag=spa"', html)

    def test_falls_back_to_get_absolute_url_when_reversible(self):
        html = render("tags", tags=[Tag("Spa", "spa", url="/tag/spa/")])
        self.assertIn('href="/tag/spa/"', html)

    def test_unreversible_get_absolute_url_renders_span(self):
        html = render("tags", tags=[Tag("Spa", "spa")])
        self.assertNotIn("<a ", html)
        self.assertIn("hashtag-chip", html)

    def test_accepts_plain_strings(self):
        html = render('tags linkable=False prefix="#"', tags=["calm", "quiet"])
        self.assertIn("#calm", html)
        self.assertIn("#quiet", html)

    def test_empty_renders_nothing(self):
        self.assertEqual(render("tags", tags=[]).strip(), "")

    def test_link_class_and_placement_applied(self):
        html = render(
            'tags href_pattern="/r/?tag={slug}" link_class="review-channel-click" placement="review_modal"',
            tags=[Tag("Cozy", "cozy")],
        )
        self.assertIn("review-channel-click", html)
        self.assertIn('data-placement="review_modal"', html)
        self.assertIn('data-channel="tag"', html)

    def test_tag_name_markup_is_escaped(self):
        html = render(
            "tags linkable=False",
            tags=[Tag("<script>x</script>", "x")],
        )
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_label_marks_container_and_items_as_list(self):
        html = render(
            'tags label="Tags" href_pattern="/r/?tag={slug}"',
            tags=[Tag("Cozy", "cozy")],
        )
        self.assertIn('role="list"', html)
        self.assertIn('aria-label="Tags"', html)
        self.assertIn('role="listitem"', html)
