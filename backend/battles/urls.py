from django.urls import path

from . import views

app_name = "battles"

urlpatterns = [
    path("", views.BattleList.as_view(), name="battle_list"),
    path("add", views.BattleCreate.as_view(), name="battle_create"),
    path("<int:pk>", views.BattleDetail.as_view(), name="battle_detail"),
    path(
        "<int:pk>/opponent-pokemons",
        views.BattleUpdateOpponentPokemons.as_view(),
        name="battle_update_opponent_pokemons",
    ),
    path("settled", views.SettledBattlesList.as_view(), name="settled_battles_list"),
]
