from rest_framework import serializers

from api.battles.validators import validate_pokemon
from battles.models import Battle
from pokemons.exceptions import PokemonNotFound
from pokemons.helpers import get_pokemons_points_sum


class BattleSerializer(serializers.ModelSerializer):
    creator_pokemon_1 = serializers.CharField()
    creator_pokemon_2 = serializers.CharField()
    creator_pokemon_3 = serializers.CharField()

    opponent_pokemon_1 = serializers.CharField(required=False)
    opponent_pokemon_2 = serializers.CharField(required=False)
    opponent_pokemon_3 = serializers.CharField(required=False)

    class Meta:
        model = Battle
        fields = (
            "id",
            "creator",
            "opponent",
            "creator_pokemon_1",
            "creator_pokemon_2",
            "creator_pokemon_3",
            "opponent_pokemon_1",
            "opponent_pokemon_2",
            "opponent_pokemon_3",
        )

    def validate_creator_pokemon_1(self, value):
        return validate_pokemon(value)

    def validate_creator_pokemon_2(self, value):
        return validate_pokemon(value)

    def validate_creator_pokemon_3(self, value):
        return validate_pokemon(value)

    def validate_opponent_pokemon_1(self, value):
        return validate_pokemon(value)

    def validate_opponent_pokemon_2(self, value):
        return validate_pokemon(value)

    def validate_opponent_pokemon_3(self, value):
        return validate_pokemon(value)

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

        if self.instance:
            if request.user != self.instance.opponent:
                raise serializers.ValidationError(
                    "You can't update opponent Pokemons if you aren't the battle opponent"
                )

            opponent_pokemon_1 = attrs.get("opponent_pokemon_1")
            opponent_pokemon_2 = attrs.get("opponent_pokemon_2")
            opponent_pokemon_3 = attrs.get("opponent_pokemon_3")

            pokemon_points_sum = 0
            try:
                pokemon_points_sum = get_pokemons_points_sum(
                    [opponent_pokemon_1.name, opponent_pokemon_2.name, opponent_pokemon_3.name]
                )
            except PokemonNotFound:
                pass

            if pokemon_points_sum > 600:
                raise serializers.ValidationError("Pokemons' points sum cannot be more than 600")

        return attrs

    def create(self, validated_data):
        return Battle.objects.create(**validated_data)

    def update(self, instance, validated_data):  # noqa
        instance = super().update(instance, validated_data)

        opponent_pokemon_1 = self.validated_data.pop("opponent_pokemon_1", None)
        opponent_pokemon_2 = self.validated_data.pop("opponent_pokemon_2", None)
        opponent_pokemon_3 = self.validated_data.pop("opponent_pokemon_3", None)

        opponent_pokemons = [opponent_pokemon_1, opponent_pokemon_2, opponent_pokemon_3]

        if not any(pokemon is None for pokemon in opponent_pokemons):
            return

        instance.opponent_pokemon_1 = opponent_pokemon_1
        instance.opponent_pokemon_2 = opponent_pokemon_2
        instance.opponent_pokemon_3 = opponent_pokemon_3
        instance.save()

        return instance
