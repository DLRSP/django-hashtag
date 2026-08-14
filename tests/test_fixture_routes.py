"""Security contracts for test URL fixtures (no reflected user input)."""

from django.test import Client, SimpleTestCase


class TaggedFixtureRouteTests(SimpleTestCase):
    def test_tagged_route_does_not_reflect_slug(self):
        """Reversal fixture must never echo the path slug into the body."""
        client = Client()
        probe = "xss-probe-slug"
        response = client.get(f"/tag/{probe}/")
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertEqual(body, "ok")
        self.assertNotIn(probe, body)
        self.assertNotIn("<script", body.lower())
