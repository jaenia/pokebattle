from rest_framework import serializers

from pokemons.models import Pokemon
from pokemons.services import pokemon_exists


def validate_pokemon(pokemon_name):
    if not pokemon_exists(pokemon_name):
        raise serializers.ValidationError("Sorry, this pokemon was not found")
    return Pokemon.objects.get(name=pokemon_name)
