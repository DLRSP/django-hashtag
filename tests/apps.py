"""Django app config so deepen ORM fixtures are synced by the harness."""

from django.apps import AppConfig


class TestsConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "tests"
    label = "hashtag_tests"
    verbose_name = "hashtag test models"
