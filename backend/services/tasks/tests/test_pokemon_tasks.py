import responses
from django.test import TestCase
from model_mommy import mommy

from common.constants import POKEAPI_BASE_URL
from pokemons.models import Pokemon
from services.tasks import pokemon_tasks


class SaveAllPokemonsFromPokeAPITaskTests(TestCase):
    @responses.activate
    def test_save_all_pokemons_from_pokeapi(self):
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
            f"{POKEAPI_BASE_URL}pokemon?limit=60",
            status=200,
            json={
                "count": 3,
                "next": None,
                "previous": None,
                "results": [pokemon_1, pokemon_2, pokemon_3],
            },
        )

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/pokemon1",
            status=200,
            json=pokemon_1,
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/pokemon2",
            status=200,
            json=pokemon_2,
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/pokemon3",
            status=200,
            json=pokemon_3,
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
            f"{POKEAPI_BASE_URL}pokemon?limit=60",
            status=200,
            json={
                "count": 2,
                "next": None,
                "previous": None,
                "results": [pokemon_1, pokemon_2],
            },
        )

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/pokemon1",
            status=200,
            json=pokemon_1,
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/pokemon2",
            status=200,
            json=pokemon_2,
        )

        pokemon_tasks.save_all_pokemons_from_pokeapi()

        pokemons = Pokemon.objects.all()
        self.assertEqual(len(pokemons), 1)

        pokemons_ids = [pokemon.poke_id for pokemon in pokemons]
        self.assertIn(pokemon_1["id"], pokemons_ids)
        self.assertNotIn(pokemon_2["id"], pokemons_ids)

    @responses.activate
    def test_update_existing_pokemons(self):
        mommy.make(
            "pokemons.Pokemon",
            poke_id=1,
            name="pokemon1",
            attack=49,
            defense=49,
            hit_points=45,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/1.png",
        )
        mommy.make(
            "pokemons.Pokemon",
            poke_id=2,
            name="pokemon2",
            attack=64,
            defense=64,
            hit_points=50,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/2.png",
        )

        # pokemons 1 and 2 with new image links
        api_pokemon_1 = {
            "id": 1,
            "name": "pokemon1",
            "stats": [{"base_stat": 45}, {"base_stat": 49}, {"base_stat": 49}],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/"
                "PokeAPI/sprites/master/sprites/pokemon/new-link-1.png"
            },
        }
        api_pokemon_2 = {
            "id": 2,
            "name": "pokemon2",
            "stats": [{"base_stat": 50}, {"base_stat": 64}, {"base_stat": 64}],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/"
                "PokeAPI/sprites/master/sprites/pokemon/new-link-2.png"
            },
        }
        api_pokemon_3 = {
            "id": 3,
            "name": "pokemon3",
            "stats": [{"base_stat": 55}, {"base_stat": 69}, {"base_stat": 69}],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/"
                "PokeAPI/sprites/master/sprites/pokemon/new-link-3.png"
            },
        }

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon?limit=60",
            status=200,
            json={
                "count": 3,
                "next": None,
                "previous": None,
                "results": [api_pokemon_1, api_pokemon_2, api_pokemon_3],
            },
        )

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/pokemon1",
            status=200,
            json=api_pokemon_1,
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/pokemon2",
            status=200,
            json=api_pokemon_2,
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/pokemon3",
            status=200,
            json=api_pokemon_3,
        )

        pokemon_1 = Pokemon.objects.filter(name="pokemon1").first()
        pokemon_2 = Pokemon.objects.filter(name="pokemon2").first()
        pokemon_3 = Pokemon.objects.filter(name="pokemon3").first()

        self.assertEqual(
            pokemon_1.image,
            "https://raw.githubusercontent.com/" "PokeAPI/sprites/master/sprites/pokemon/1.png",
        )
        self.assertEqual(
            pokemon_2.image,
            "https://raw.githubusercontent.com/" "PokeAPI/sprites/master/sprites/pokemon/2.png",
        )
        self.assertIsNone(pokemon_3)

        pokemon_tasks.save_all_pokemons_from_pokeapi()

        pokemons = Pokemon.objects.all()
        self.assertEqual(len(pokemons), 3)

        pokemon_1 = Pokemon.objects.filter(name="pokemon1").first()
        pokemon_2 = Pokemon.objects.filter(name="pokemon2").first()
        pokemon_3 = Pokemon.objects.filter(name="pokemon3").first()

        self.assertEqual(
            pokemon_1.image.name,
            "https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/new-link-1.png",
        )
        self.assertEqual(
            pokemon_2.image.name,
            "https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/new-link-2.png",
        )
        self.assertEqual(
            pokemon_3.image.name,
            "https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/new-link-3.png",
        )
