"""Tests for MyTag.get_absolute_url opt-in routing."""

from django.test import SimpleTestCase, override_settings
from django.urls import NoReverseMatch

from hashtag.models import MyTag


class TagAbsoluteUrlTest(SimpleTestCase):
    def test_uses_configured_route_name(self):
        tag = MyTag(name="Spa", slug="spa")
        with override_settings(HASHTAG_TAG_URL_NAME="tagged"):
            self.assertEqual(tag.get_absolute_url(), "/tag/spa/")

    def test_defaults_to_tagged_route(self):
        tag = MyTag(name="Spa", slug="spa")
        self.assertEqual(tag.get_absolute_url(), "/tag/spa/")

    def test_disabled_when_url_name_blank(self):
        tag = MyTag(name="Spa", slug="spa")
        with override_settings(HASHTAG_TAG_URL_NAME=""):
            with self.assertRaises(NoReverseMatch):
                tag.get_absolute_url()
