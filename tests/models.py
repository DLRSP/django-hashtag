"""Concrete models for exercising filter_queryset_by_tag join distinctness."""

from django.db import models


class ChipTarget(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ChipLabel(models.Model):
    """Non-unique slug so two labels can share a slug and multiply joins."""

    slug = models.SlugField()
    targets = models.ManyToManyField(ChipTarget, related_name="labels")

    def __str__(self):
        return self.slug
