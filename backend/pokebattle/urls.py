from django.conf.urls import include, url  # noqa
from django.urls import path
from django.contrib import admin

import django_js_reverse.views


urlpatterns = [
    path("", include("battles.urls", namespace="battles")),
    path("user/", include("users.urls", namespace="users")),
    path("pokemon/", include("pokemons.urls", namespace="pokemons")),
    path("admin/", admin.site.urls, name="admin"),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("api/user/", include("users.urls")),
]
