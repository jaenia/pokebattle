from django.test import TestCase

from model_mommy import mommy

from battles.forms import BattleForm


class BattleCreateFormTests(TestCase):
    def test_create_battle(self):
        current_user = mommy.make("users.User")
        opponent = mommy.make("users.User", email="opponent@test.com")

        pokemon1 = mommy.make("pokemons.Pokemon", poke_id=1)
        pokemon2 = mommy.make("pokemons.Pokemon", poke_id=2)
        pokemon3 = mommy.make("pokemons.Pokemon", poke_id=3)

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1_input": pokemon1.poke_id,
            "creator_pokemon_2_input": pokemon2.poke_id,
            "creator_pokemon_3_input": pokemon3.poke_id,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertTrue(form.is_valid())

        battle = form.save()
        self.assertEqual(battle.creator, current_user)
        self.assertEqual(battle.opponent, opponent)
        self.assertEqual(battle.creator_pokemon_1, pokemon1)
        self.assertEqual(battle.creator_pokemon_2, pokemon2)
        self.assertEqual(battle.creator_pokemon_3, pokemon3)

    def test_cannot_create_battle_with_creator_as_opponent(self):
        current_user = mommy.make("users.User")

        pokemon1 = mommy.make("pokemons.Pokemon", poke_id=1)
        pokemon2 = mommy.make("pokemons.Pokemon", poke_id=2)
        pokemon3 = mommy.make("pokemons.Pokemon", poke_id=3)

        data = {
            "opponent": current_user.id,
            "creator_pokemon_1_input": pokemon1.poke_id,
            "creator_pokemon_2_input": pokemon2.poke_id,
            "creator_pokemon_3_input": pokemon3.poke_id,
        }

        form = BattleForm(data=data, current_user=current_user)

        self.assertFalse(form.is_valid())
        self.assertIn("opponent", form.errors)

    def test_cannot_force_a_creator_user(self):
        current_user = mommy.make("users.User")
        fake_creator_user = mommy.make("users.User")
        opponent = mommy.make("users.User")

        pokemon1 = mommy.make("pokemons.Pokemon", poke_id=1)
        pokemon2 = mommy.make("pokemons.Pokemon", poke_id=2)
        pokemon3 = mommy.make("pokemons.Pokemon", poke_id=3)

        data = {
            "creator": fake_creator_user.id,
            "opponent": opponent.id,
            "creator_pokemon_1_input": pokemon1.poke_id,
            "creator_pokemon_2_input": pokemon2.poke_id,
            "creator_pokemon_3_input": pokemon3.poke_id,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertTrue(form.is_valid())

        battle = form.save()
        self.assertEqual(battle.creator, current_user)

    def test_cannot_create_battle_if_pokemon_does_not_exist_in_api(self):
        current_user = mommy.make("users.User")
        opponent = mommy.make("users.User", email="opponent@test.com")

        pokemon1 = mommy.make("pokemons.Pokemon", poke_id=0)
        pokemon2 = mommy.make("pokemons.Pokemon", poke_id=1)
        pokemon3 = mommy.make("pokemons.Pokemon", poke_id=2)

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1_input": pokemon1.poke_id,
            "creator_pokemon_2_input": pokemon2.poke_id,
            "creator_pokemon_3_input": pokemon3.poke_id,
        }

        form = BattleForm(data=data, current_user=current_user)
        self.assertFalse(form.is_valid())

        self.assertIn("creator_pokemon_1_input", form.errors)
