from django.conf.urls import include, url  # noqa
from django.urls import path
from django.contrib import admin

import django_js_reverse.views


urlpatterns = [
    path("", include("battles.urls")),
    path("admin/", admin.site.urls, name="admin"),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
]
