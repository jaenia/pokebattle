import responses

from django.test import TestCase

from model_mommy import mommy

from battles.forms import BattleForm, BattleOpponentPokemonsForm
from common.constants import POKEAPI_BASE_URL


class BattleCreateFormTests(TestCase):
    @responses.activate
    def test_create_battle(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon3", status=200)

        pokemon_1 = mommy.make(
            "pokemons.Pokemon",
            poke_id=1,
            name="pokemon1",
            attack=49,
            defense=49,
            hit_points=45,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/1.png",
        )
        pokemon_2 = mommy.make(
            "pokemons.Pokemon",
            poke_id=2,
            name="pokemon2",
            attack=64,
            defense=64,
            hit_points=50,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/2.png",
        )
        pokemon_3 = mommy.make(
            "pokemons.Pokemon",
            poke_id=3,
            name="pokemon3",
            attack=69,
            defense=69,
            hit_points=55,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/3.png",
        )

        current_user = mommy.make("users.User")
        opponent = mommy.make("users.User", email="opponent@test.com")

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1": pokemon_1.id,
            "creator_pokemon_2": pokemon_2.id,
            "creator_pokemon_3": pokemon_3.id,
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
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon3", status=200)

        pokemon_1 = mommy.make(
            "pokemons.Pokemon",
            poke_id=1,
            name="pokemon1",
            attack=49,
            defense=49,
            hit_points=45,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/1.png",
        )
        pokemon_2 = mommy.make(
            "pokemons.Pokemon",
            poke_id=2,
            name="pokemon2",
            attack=64,
            defense=64,
            hit_points=50,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/2.png",
        )
        pokemon_3 = mommy.make(
            "pokemons.Pokemon",
            poke_id=3,
            name="pokemon3",
            attack=69,
            defense=69,
            hit_points=55,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/3.png",
        )

        current_user = mommy.make("users.User")

        data = {
            "opponent": current_user.id,
            "creator_pokemon_1": pokemon_1.id,
            "creator_pokemon_2": pokemon_2.id,
            "creator_pokemon_3": pokemon_3.id,
        }

        form = BattleForm(data=data, current_user=current_user)

        self.assertFalse(form.is_valid())
        self.assertIn("opponent", form.errors)

    @responses.activate
    def test_cannot_force_a_creator_user(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon3", status=200)

        pokemon_1 = mommy.make(
            "pokemons.Pokemon",
            poke_id=1,
            name="pokemon1",
            attack=49,
            defense=49,
            hit_points=45,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/1.png",
        )
        pokemon_2 = mommy.make(
            "pokemons.Pokemon",
            poke_id=2,
            name="pokemon2",
            attack=64,
            defense=64,
            hit_points=50,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/2.png",
        )
        pokemon_3 = mommy.make(
            "pokemons.Pokemon",
            poke_id=3,
            name="pokemon3",
            attack=69,
            defense=69,
            hit_points=55,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/3.png",
        )

        current_user = mommy.make("users.User")
        fake_creator_user = mommy.make("users.User")
        opponent = mommy.make("users.User")

        data = {
            "creator": fake_creator_user.id,
            "opponent": opponent.id,
            "creator_pokemon_1": pokemon_1.id,
            "creator_pokemon_2": pokemon_2.id,
            "creator_pokemon_3": pokemon_3.id,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertTrue(form.is_valid())

        battle = form.save()
        self.assertEqual(battle.creator, current_user)

    @responses.activate
    def test_cannot_create_battle_if_pokemon_points_sum_more_than_600(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon3", status=200)

        pokemon_1 = mommy.make(
            "pokemons.Pokemon",
            poke_id=1,
            name="pokemon1",
            attack=100,
            defense=100,
            hit_points=100,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/1.png",
        )
        pokemon_2 = mommy.make(
            "pokemons.Pokemon",
            poke_id=2,
            name="pokemon2",
            attack=100,
            defense=100,
            hit_points=100,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/2.png",
        )
        pokemon_3 = mommy.make(
            "pokemons.Pokemon",
            poke_id=3,
            name="pokemon3",
            attack=100,
            defense=100,
            hit_points=100,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/3.png",
        )

        current_user = mommy.make("users.User")
        opponent = mommy.make("users.User", email="opponent@test.com")

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1": pokemon_1.id,
            "creator_pokemon_2": pokemon_2.id,
            "creator_pokemon_3": pokemon_3.id,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertFalse(form.is_valid())

        self.assertEqual(["Pokemons' points sum cannot be more than 600"], form.errors["__all__"])


class BattleOpponentPokemonsFormTests(TestCase):
    @responses.activate
    def test_cannot_create_battle_if_pokemon_points_sum_more_than_600(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon3", status=200)

        pokemon_1 = mommy.make(
            "pokemons.Pokemon",
            poke_id=1,
            name="pokemon1",
            attack=100,
            defense=100,
            hit_points=100,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/1.png",
        )
        pokemon_2 = mommy.make(
            "pokemons.Pokemon",
            poke_id=2,
            name="pokemon2",
            attack=100,
            defense=100,
            hit_points=100,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/2.png",
        )
        pokemon_3 = mommy.make(
            "pokemons.Pokemon",
            poke_id=3,
            name="pokemon3",
            attack=100,
            defense=100,
            hit_points=100,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/3.png",
        )

        data = {
            "opponent_pokemon_1": pokemon_1.id,
            "opponent_pokemon_2": pokemon_2.id,
            "opponent_pokemon_3": pokemon_3.id,
        }

        form = BattleOpponentPokemonsForm(data=data)
        self.assertFalse(form.is_valid())

        self.assertEqual(["Pokemons' points sum cannot be more than 600"], form.errors["__all__"])
