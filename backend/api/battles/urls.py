from django.urls import path

from . import views

urlpatterns = [
    path("", views.BattleListCreateEndpoint.as_view(), name="battles"),
]
