"""ORM + signal integration for hashtag counts."""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils import timezone

from hashtag.models import MyTag, MyTaggedItem, MyTagGroup


class HashtagOrmSignalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = MyTagGroup.objects.create(name="Default", slug="default")

    def test_tag_slug_from_name_on_create(self):
        tag = MyTag.objects.create(name="Sea View", group=self.group)
        self.assertEqual(tag.slug, "sea-view")

    def test_tagged_item_increments_count(self):
        tag = MyTag.objects.create(name="Spa", group=self.group, count=0)
        user = get_user_model().objects.create_user("u1", password="x")
        ct = ContentType.objects.get_for_model(user)
        MyTaggedItem.objects.create(
            tag=tag, content_type=ct, object_id=user.pk
        )
        tag.refresh_from_db()
        self.assertEqual(tag.count, 1)
        self.assertIsNotNone(tag.last_used)
        self.assertTrue(timezone.is_aware(tag.last_used))

    def test_tagged_item_delete_decrements_count(self):
        tag = MyTag.objects.create(name="Pool", group=self.group, count=0)
        user = get_user_model().objects.create_user("u2", password="x")
        ct = ContentType.objects.get_for_model(user)
        item = MyTaggedItem.objects.create(
            tag=tag, content_type=ct, object_id=user.pk
        )
        item.delete()
        tag.refresh_from_db()
        self.assertEqual(tag.count, 0)
        self.assertTrue(timezone.is_aware(tag.last_used))

    def test_tagged_item_links_content_object(self):
        tag = MyTag.objects.create(name="Calm", group=self.group)
        user = get_user_model().objects.create_user("u3", password="x")
        other = get_user_model().objects.create_user("u4", password="x")
        ct = ContentType.objects.get_for_model(user)
        MyTaggedItem.objects.create(
            tag=tag, content_type=ct, object_id=user.pk
        )
        tagged_ids = list(
            MyTaggedItem.objects.filter(tag__slug="calm").values_list(
                "object_id", flat=True
            )
        )
        self.assertIn(user.pk, tagged_ids)
        self.assertNotIn(other.pk, tagged_ids)
