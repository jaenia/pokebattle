from django.urls import path

from pokemons.views import PokemonAutocomplete

app_name = "pokemons"

urlpatterns = [
    path("pokemon-autocomplete", PokemonAutocomplete.as_view(), name='pokemon_autocomplete'),
]
