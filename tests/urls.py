"""Test urls for django-hashtag.

Defines the ``tagged`` route name that ``MyTag.get_absolute_url`` reverses,
so model and template-tag behaviour can be exercised in isolation.
"""

from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse
from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog


def tagged(request, slug):
    # Reversal-only fixture: ``MyTag.get_absolute_url`` reverses the ``tagged``
    # route name; no test inspects the body. Do NOT echo the user-provided slug
    # back in the response — that is reflected XSS (CWE-79) and CodeQL flags it.
    return HttpResponse("ok")


urlpatterns = [
    path("tag/<slug:slug>/", tagged, name="tagged"),
]

urlpatterns += i18n_patterns(
    re_path(
        r"^jsi18n/$", JavaScriptCatalog.as_view(), name="javascript-catalog"
    ),
)
