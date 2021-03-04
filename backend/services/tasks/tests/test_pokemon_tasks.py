import responses
from django.test import TestCase

from common.constants import POKEAPI_BASE_URL, POKEAPI_POKEMONS_LIMIT
from pokemons.models import Pokemon
from services.tasks import pokemon_tasks


class SaveAllPokemonsFromPokeAPITaskTests(TestCase):
    @responses.activate
    def test_save_all_pokemons_from_poke_api(self):
        pokemon_1 = {
            "id": 1,
            "name": "pokemon1",
            "stats": [{"base_stat": 45}, {"base_stat": 49}, {"base_stat": 49}],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/"
                "PokeAPI/sprites/master/sprites/pokemon/1.png"
            },
        }
        pokemon_2 = {
            "id": 2,
            "name": "pokemon2",
            "stats": [{"base_stat": 50}, {"base_stat": 64}, {"base_stat": 64}],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/"
                "PokeAPI/sprites/master/sprites/pokemon/2.png"
            },
        }
        pokemon_3 = {
            "id": 2,
            "name": "pokemon3",
            "stats": [{"base_stat": 55}, {"base_stat": 69}, {"base_stat": 69}],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/"
                "PokeAPI/sprites/master/sprites/pokemon/3.png"
            },
        }

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon?limit={POKEAPI_POKEMONS_LIMIT}",
            status=200,
            json={
                "count": 3,
                "next": "null",
                "previous": "null",
                "results": [pokemon_1, pokemon_2, pokemon_3],
            },
        )

        pokemon_tasks.save_all_pokemons_from_pokeapi()

        pokemons = Pokemon.objects.all()
        self.assertEqual(len(pokemons), 3)

        pokemons_ids = [pokemon.poke_id for pokemon in pokemons]
        self.assertIn(pokemon_1["id"], pokemons_ids)
        self.assertIn(pokemon_2["id"], pokemons_ids)
        self.assertIn(pokemon_3["id"], pokemons_ids)

    @responses.activate
    def test_save_all_pokemons_from_poke_api_without_duplicating_data(self):
        pokemon_1 = {
            "id": 1,
            "name": "pokemon1",
            "stats": [{"base_stat": 45}, {"base_stat": 49}, {"base_stat": 49}],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/"
                "PokeAPI/sprites/master/sprites/pokemon/1.png"
            },
        }
        pokemon_2 = {
            "id": 2,
            "name": "pokemon1",
            "stats": [{"base_stat": 45}, {"base_stat": 49}, {"base_stat": 49}],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/"
                "PokeAPI/sprites/master/sprites/pokemon/1.png"
            },
        }

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon?limit={POKEAPI_POKEMONS_LIMIT}",
            status=200,
            json={
                "count": 2,
                "next": "null",
                "previous": "null",
                "results": [pokemon_1, pokemon_2],
            },
        )

        pokemon_tasks.save_all_pokemons_from_pokeapi()

        pokemons = Pokemon.objects.all()
        self.assertEqual(len(pokemons), 1)

        pokemons_ids = [pokemon.poke_id for pokemon in pokemons]
        self.assertIn(pokemon_1["id"], pokemons_ids)
        self.assertNotIn(pokemon_2["id"], pokemons_ids)
