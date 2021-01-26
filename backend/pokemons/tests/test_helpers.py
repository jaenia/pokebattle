import responses
from django.test import TestCase
from model_mommy import mommy

from common.constants import POKEAPI_BASE_URL
from pokemons.exceptions import PokemonNotFound
from pokemons.helpers import get_pokemons_points_sum


class PokemonHelperTests(TestCase):
    @responses.activate
    def test_raises_exception_if_pokemon_does_not_exist_when_calculating_points_sum(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/0", status=404)

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/0",
            status=404,
            json={"error": "not found"},
        )

        mommy.make("pokemons.Pokemon", poke_id=1)
        mommy.make("pokemons.Pokemon", poke_id=2)

        with self.assertRaises(PokemonNotFound):
            get_pokemons_points_sum([0, 1, 2])
