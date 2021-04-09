from django.urls import path

from . import views

urlpatterns = [
    path("", views.PokemonListEndpoint.as_view(), name="pokemon_list"),
]
