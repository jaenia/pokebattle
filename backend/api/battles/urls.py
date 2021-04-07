from django.urls import path

from . import views

urlpatterns = [
    path("", views.BattleListCreateEndpoint.as_view(), name="battle_list_create"),
    path("<int:pk>", views.BattleRetrieveUpdateEndpoint.as_view(), name="battle_retrieve_update"),
]
