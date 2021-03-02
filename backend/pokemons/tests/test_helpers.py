import responses
from django.test import TestCase
from model_mommy import mommy

from common.constants import POKEAPI_BASE_URL
from pokemons.exceptions import PokemonNotFound
from pokemons.helpers import get_pokemons_points_sum, save_pokemon


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

    @responses.activate
    def test_save_pokemon_image(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/1", status=200)

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/1",
            status=200,
            json={
                "id": 1,
                "name": "pokemon1",
                "stats": [{"base_stat": 45}, {"base_stat": 49}, {"base_stat": 49}],
                "sprites": {
                    "front_default": "https://raw.githubusercontent.com/P"
                    "okeAPI/sprites/master/sprites/pokemon/1.png"
                },
            },
        )

        pokemon = save_pokemon(1)
        self.assertEqual(
            pokemon.image,
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        )
