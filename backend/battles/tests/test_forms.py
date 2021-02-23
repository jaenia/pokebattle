import responses

from django.test import TestCase

from model_mommy import mommy

from battles.forms import BattleForm, BattleOpponentPokemonsForm
from common.constants import POKEAPI_BASE_URL


class BattleCreateFormTests(TestCase):
    @responses.activate
    def test_create_battle(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/3", status=200)

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/1",
            status=200,
            json={
                "id": 1,
                "name": "pokemon1",
                "stats": [{"base_stat": 45}, {"base_stat": 49}, {"base_stat": 49}],
                "sprites": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
                },
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/2",
            status=200,
            json={
                "id": 2,
                "name": "pokemon2",
                "stats": [{"base_stat": 50}, {"base_stat": 64}, {"base_stat": 64}],
                "sprites": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png"
                },
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/3",
            status=200,
            json={
                "id": 3,
                "name": "pokemon3",
                "stats": [{"base_stat": 55}, {"base_stat": 69}, {"base_stat": 69}],
                "sprites": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png"
                },
            },
        )

        current_user = mommy.make("users.User")
        opponent = mommy.make("users.User", email="opponent@test.com")

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1_input": 1,
            "creator_pokemon_2_input": 2,
            "creator_pokemon_3_input": 3,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertTrue(form.is_valid())

        battle = form.save()
        self.assertEqual(battle.creator, current_user)
        self.assertEqual(battle.opponent, opponent)
        self.assertEqual(battle.creator_pokemon_1.poke_id, 1)
        self.assertEqual(battle.creator_pokemon_2.poke_id, 2)
        self.assertEqual(battle.creator_pokemon_3.poke_id, 3)

    @responses.activate
    def test_cannot_create_battle_with_creator_as_opponent(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/3", status=200)

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/1",
            status=200,
            json={
                "id": 1,
                "name": "pokemon1",
                "stats": [{"base_stat": 45}, {"base_stat": 49}, {"base_stat": 49}],
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/2",
            status=200,
            json={
                "id": 2,
                "name": "pokemon2",
                "stats": [{"base_stat": 50}, {"base_stat": 64}, {"base_stat": 64}],
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/3",
            status=200,
            json={
                "id": 3,
                "name": "pokemon3",
                "stats": [{"base_stat": 55}, {"base_stat": 69}, {"base_stat": 69}],
            },
        )

        current_user = mommy.make("users.User")

        data = {
            "opponent": current_user.id,
            "creator_pokemon_1_input": 1,
            "creator_pokemon_2_input": 2,
            "creator_pokemon_3_input": 3,
        }

        form = BattleForm(data=data, current_user=current_user)

        self.assertFalse(form.is_valid())
        self.assertIn("opponent", form.errors)

    @responses.activate
    def test_cannot_force_a_creator_user(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/3", status=200)

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/1",
            status=200,
            json={
                "id": 1,
                "name": "pokemon1",
                "stats": [{"base_stat": 45}, {"base_stat": 49}, {"base_stat": 49}],
                "sprites": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
                },
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/2",
            status=200,
            json={
                "id": 2,
                "name": "pokemon2",
                "stats": [{"base_stat": 50}, {"base_stat": 64}, {"base_stat": 64}],
                "sprites": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png"
                },
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/3",
            status=200,
            json={
                "id": 3,
                "name": "pokemon3",
                "stats": [{"base_stat": 55}, {"base_stat": 69}, {"base_stat": 69}],
                "sprites": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/3.png"
                },
            },
        )

        current_user = mommy.make("users.User")
        fake_creator_user = mommy.make("users.User")
        opponent = mommy.make("users.User")

        data = {
            "creator": fake_creator_user.id,
            "opponent": opponent.id,
            "creator_pokemon_1_input": 1,
            "creator_pokemon_2_input": 2,
            "creator_pokemon_3_input": 3,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertTrue(form.is_valid())

        battle = form.save()
        self.assertEqual(battle.creator, current_user)

    @responses.activate
    def test_cannot_create_battle_if_pokemon_does_not_exist_in_api(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/0", status=404)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/2", status=200)

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/0",
            status=404,
            json={"error": "not found"},
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/1",
            status=200,
            json={
                "id": 1,
                "name": "pokemon1",
                "stats": [{"base_stat": 45}, {"base_stat": 49}, {"base_stat": 49}],
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/2",
            status=200,
            json={
                "id": 2,
                "name": "pokemon2",
                "stats": [{"base_stat": 50}, {"base_stat": 64}, {"base_stat": 64}],
            },
        )

        current_user = mommy.make("users.User")
        opponent = mommy.make("users.User", email="opponent@test.com")

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1_input": 0,
            "creator_pokemon_2_input": 1,
            "creator_pokemon_3_input": 2,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertFalse(form.is_valid())

        self.assertIn("creator_pokemon_1_input", form.errors)

    @responses.activate
    def test_cannot_create_battle_if_pokemon_points_sum_more_than_600(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/3", status=200)

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/1",
            status=200,
            json={
                "id": 1,
                "name": "pokemon1",
                "stats": [{"base_stat": 100}, {"base_stat": 100}, {"base_stat": 100}],
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/2",
            status=200,
            json={
                "id": 2,
                "name": "pokemon2",
                "stats": [{"base_stat": 100}, {"base_stat": 100}, {"base_stat": 100}],
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/3",
            status=200,
            json={
                "id": 3,
                "name": "pokemon3",
                "stats": [{"base_stat": 100}, {"base_stat": 100}, {"base_stat": 100}],
            },
        )

        current_user = mommy.make("users.User")
        opponent = mommy.make("users.User", email="opponent@test.com")

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1_input": 1,
            "creator_pokemon_2_input": 2,
            "creator_pokemon_3_input": 3,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertFalse(form.is_valid())

        self.assertEqual(["Pokemons' points sum cannot be more than 600"], form.errors["__all__"])


class BattleOpponentPokemonsFormTests(TestCase):
    @responses.activate
    def test_cannot_create_battle_if_pokemon_does_not_exist_in_api(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/0", status=404)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/2", status=200)

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/0",
            status=404,
            json={"error": "not found"},
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/1",
            status=200,
            json={
                "id": 1,
                "name": "pokemon1",
                "stats": [{"base_stat": 45}, {"base_stat": 49}, {"base_stat": 49}],
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/2",
            status=200,
            json={
                "id": 2,
                "name": "pokemon2",
                "stats": [{"base_stat": 50}, {"base_stat": 64}, {"base_stat": 64}],
            },
        )

        data = {
            "opponent_pokemon_1_input": 0,
            "opponent_pokemon_2_input": 1,
            "opponent_pokemon_3_input": 2,
        }

        form = BattleOpponentPokemonsForm(data=data)
        self.assertFalse(form.is_valid())

        self.assertIn("opponent_pokemon_1_input", form.errors)

    @responses.activate
    def test_cannot_create_battle_if_pokemon_points_sum_more_than_600(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/3", status=200)

        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/1",
            status=200,
            json={
                "id": 1,
                "name": "pokemon1",
                "stats": [{"base_stat": 100}, {"base_stat": 100}, {"base_stat": 100}],
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/2",
            status=200,
            json={
                "id": 2,
                "name": "pokemon2",
                "stats": [{"base_stat": 100}, {"base_stat": 100}, {"base_stat": 100}],
            },
        )
        responses.add(
            responses.GET,
            f"{POKEAPI_BASE_URL}pokemon/3",
            status=200,
            json={
                "id": 3,
                "name": "pokemon3",
                "stats": [{"base_stat": 100}, {"base_stat": 100}, {"base_stat": 100}],
            },
        )

        data = {
            "opponent_pokemon_1_input": 1,
            "opponent_pokemon_2_input": 2,
            "opponent_pokemon_3_input": 3,
        }

        form = BattleOpponentPokemonsForm(data=data)
        self.assertFalse(form.is_valid())

        self.assertEqual(["Pokemons' points sum cannot be more than 600"], form.errors["__all__"])
