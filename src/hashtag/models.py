from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from taggit.models import GenericTaggedItemBase, TagBase


class MyTagGroup(TagBase):
    name = models.CharField(verbose_name=_("Name"), unique=True, max_length=100)
    slug = models.SlugField(verbose_name=_("Slug"), unique=True, max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class MyTag(TagBase):
    group = models.ForeignKey(
        MyTagGroup, on_delete=models.PROTECT, verbose_name=_("Group"), default=1
    )
    active = models.BooleanField(default=True)
    count = models.IntegerField(null=True, blank=True, default=0)
    last_used = models.DateTimeField(
        null=True,
        blank=True,
        default=timezone.make_aware(timezone.datetime(2000, 1, 1, 00, 00)),
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Opt-in: a tag has a canonical page only when the project names the
        # route via HASHTAG_TAG_URL_NAME. Sites that surface tags as an
        # in-context filter (?tag=slug) leave it unset and build links with
        # the hashtag_chips ``filter_url`` argument instead.
        url_name = getattr(settings, "HASHTAG_TAG_URL_NAME", "tagged")
        if not url_name:
            raise NoReverseMatch("HASHTAG_TAG_URL_NAME is not configured")
        return reverse(url_name, args=[str(self.slug)])


class MyTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(
        MyTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
    published = models.DateTimeField(
        editable=False, null=True, auto_now_add=True
    )
