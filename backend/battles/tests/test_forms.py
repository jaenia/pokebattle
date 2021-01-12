from django.test import TestCase

from model_mommy import mommy

from battles.forms import BattleForm


class BattleCreateFormTests(TestCase):
    def test_create_battle(self):
        current_user = mommy.make("users.User")
        opponent = mommy.make("users.User", email="opponent@test.com")

        creator_pokemon_1 = mommy.make("pokemons.Pokemon", poke_id=1)
        creator_pokemon_2 = mommy.make("pokemons.Pokemon", poke_id=2)
        creator_pokemon_3 = mommy.make("pokemons.Pokemon", poke_id=3)
        opponent_pokemon_1 = mommy.make("pokemons.Pokemon", poke_id=3)
        opponent_pokemon_2 = mommy.make("pokemons.Pokemon", poke_id=2)
        opponent_pokemon_3 = mommy.make("pokemons.Pokemon", poke_id=1)

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1": creator_pokemon_1.id,
            "creator_pokemon_2": creator_pokemon_2.id,
            "creator_pokemon_3": creator_pokemon_3.id,
            "opponent_pokemon_1": opponent_pokemon_1.id,
            "opponent_pokemon_2": opponent_pokemon_2.id,
            "opponent_pokemon_3": opponent_pokemon_3.id,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertTrue(form.is_valid())

        battle = form.save()
        self.assertEqual(battle.creator, current_user)
        self.assertEqual(battle.opponent, opponent)

    def test_cannot_create_battle_with_creator_as_opponent(self):
        current_user = mommy.make("users.User")
        opponent = mommy.make("users.User", email="opponent@test.com")

        creator_pokemon_1 = mommy.make("pokemons.Pokemon", poke_id=1)
        creator_pokemon_2 = mommy.make("pokemons.Pokemon", poke_id=2)
        creator_pokemon_3 = mommy.make("pokemons.Pokemon", poke_id=3)
        opponent_pokemon_1 = mommy.make("pokemons.Pokemon", poke_id=3)
        opponent_pokemon_2 = mommy.make("pokemons.Pokemon", poke_id=2)
        opponent_pokemon_3 = mommy.make("pokemons.Pokemon", poke_id=1)

        data = {
            "opponent": current_user.id,
            "creator_pokemon_1": creator_pokemon_1.id,
            "creator_pokemon_2": creator_pokemon_2.id,
            "creator_pokemon_3": creator_pokemon_3.id,
            "opponent_pokemon_1": opponent_pokemon_1.id,
            "opponent_pokemon_2": opponent_pokemon_2.id,
            "opponent_pokemon_3": opponent_pokemon_3.id,
        }

        form = BattleForm(data=data, current_user=current_user)

        self.assertFalse(form.is_valid())
        self.assertIn("opponent", form.errors)

    def test_cannot_force_a_creator_user(self):
        current_user = mommy.make("users.User")
        fake_creator_user = mommy.make("users.User")
        opponent = mommy.make("users.User")

        creator_pokemon_1 = mommy.make("pokemons.Pokemon", poke_id=1)
        creator_pokemon_2 = mommy.make("pokemons.Pokemon", poke_id=2)
        creator_pokemon_3 = mommy.make("pokemons.Pokemon", poke_id=3)
        opponent_pokemon_1 = mommy.make("pokemons.Pokemon", poke_id=3)
        opponent_pokemon_2 = mommy.make("pokemons.Pokemon", poke_id=2)
        opponent_pokemon_3 = mommy.make("pokemons.Pokemon", poke_id=1)

        data = {
            "creator": fake_creator_user.id,
            "opponent": opponent.id,
            "creator_pokemon_1": creator_pokemon_1.id,
            "creator_pokemon_2": creator_pokemon_2.id,
            "creator_pokemon_3": creator_pokemon_3.id,
            "opponent_pokemon_1": opponent_pokemon_1.id,
            "opponent_pokemon_2": opponent_pokemon_2.id,
            "opponent_pokemon_3": opponent_pokemon_3.id,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertTrue(form.is_valid())

        battle = form.save()
        self.assertEqual(battle.creator, current_user)
