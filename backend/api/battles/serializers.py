from rest_framework import serializers

from battles.models import Battle
from pokemons.exceptions import PokemonNotFound
from pokemons.helpers import get_pokemons_points_sum
from pokemons.models import Pokemon
from pokemons.services import pokemon_exists


class BattleSerializer(serializers.ModelSerializer):
    creator_pokemon_1 = serializers.CharField()
    creator_pokemon_2 = serializers.CharField()
    creator_pokemon_3 = serializers.CharField()

    class Meta:
        model = Battle
        fields = (
            "id",
            "creator",
            "opponent",
            "creator_pokemon_1",
            "creator_pokemon_2",
            "creator_pokemon_3",
        )

    def validate_creator_pokemon_1(self, value):
        if not pokemon_exists(value):
            raise serializers.ValidationError("Sorry, this pokemon was not found")
        return Pokemon.objects.get(name=value)

    def validate_creator_pokemon_2(self, value):
        if not pokemon_exists(value):
            raise serializers.ValidationError("Sorry, this pokemon was not found")
        return Pokemon.objects.get(name=value)

    def validate_creator_pokemon_3(self, value):
        if not pokemon_exists(value):
            raise serializers.ValidationError("Sorry, this pokemon was not found")
        return Pokemon.objects.get(name=value)

    def validate(self, attrs):
        request = self.context.get("request")
        attrs["creator"] = request.user

        creator_pokemon_1 = attrs.get("creator_pokemon_1")
        creator_pokemon_2 = attrs.get("creator_pokemon_2")
        creator_pokemon_3 = attrs.get("creator_pokemon_3")

        pokemon_points_sum = 0
        try:
            pokemon_points_sum = get_pokemons_points_sum(
                [creator_pokemon_1.name, creator_pokemon_2.name, creator_pokemon_3.name]
            )
        except PokemonNotFound:
            pass

        if pokemon_points_sum > 600:
            raise serializers.ValidationError("Pokemons' points sum cannot be more than 600")

        return attrs

    def create(self, validated_data):
        return Battle.objects.create(**validated_data)
