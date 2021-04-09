from rest_framework import serializers

from pokemons.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ["poke_id", "name", "attack", "defense", "hit_points", "image"]
