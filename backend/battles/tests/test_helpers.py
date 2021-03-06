from django.test import TestCase
from model_mommy import mommy

from battles.helpers import get_battle_result


class BattleHelperTests(TestCase):
    def test_creator_wins_battle(self):
        creator = mommy.make("users.User", email="creator@test.com")
        opponent = mommy.make("users.User", email="opponent@test.com")

        # creator's pokemons
        pokemon_1 = mommy.make("pokemons.Pokemon", attack=30, defense=30, hit_points=20)
        pokemon_2 = mommy.make("pokemons.Pokemon", attack=15, defense=15, hit_points=30)
        pokemon_3 = mommy.make("pokemons.Pokemon", attack=20, defense=20, hit_points=40)

        # opponent's pokemons
        pokemon_4 = mommy.make("pokemons.Pokemon", attack=20, defense=20, hit_points=35)
        pokemon_5 = mommy.make("pokemons.Pokemon", attack=10, defense=10, hit_points=30)
        pokemon_6 = mommy.make("pokemons.Pokemon", attack=25, defense=25, hit_points=50)

        battle = mommy.make(
            "battles.Battle",
            creator=creator,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
            opponent_pokemon_1=pokemon_4,
            opponent_pokemon_2=pokemon_5,
            opponent_pokemon_3=pokemon_6,
        )

        winner = get_battle_result(battle)
        self.assertEqual(winner, battle.creator)

    def test_opponent_wins_battle(self):
        creator = mommy.make("users.User", email="creator@test.com")
        opponent = mommy.make("users.User", email="opponent@test.com")

        # creator's pokemons
        pokemon_1 = mommy.make("pokemons.Pokemon", attack=10, defense=10, hit_points=20)
        pokemon_2 = mommy.make("pokemons.Pokemon", attack=5, defense=5, hit_points=15)
        pokemon_3 = mommy.make("pokemons.Pokemon", attack=20, defense=20, hit_points=40)

        # opponent's pokemons
        pokemon_4 = mommy.make("pokemons.Pokemon", attack=20, defense=20, hit_points=35)
        pokemon_5 = mommy.make("pokemons.Pokemon", attack=10, defense=10, hit_points=30)
        pokemon_6 = mommy.make("pokemons.Pokemon", attack=25, defense=25, hit_points=50)

        battle = mommy.make(
            "battles.Battle",
            creator=creator,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
            opponent_pokemon_1=pokemon_4,
            opponent_pokemon_2=pokemon_5,
            opponent_pokemon_3=pokemon_6,
        )

        winner = get_battle_result(battle)
        self.assertEqual(winner, battle.opponent)

    def test_creator_wins_battle_with_draw(self):
        creator = mommy.make("users.User", email="creator@test.com")
        opponent = mommy.make("users.User", email="opponent@test.com")

        # creator's pokemons
        pokemon_1 = mommy.make("pokemons.Pokemon", attack=10, defense=10, hit_points=20)
        pokemon_2 = mommy.make("pokemons.Pokemon", attack=15, defense=15, hit_points=40)
        pokemon_3 = mommy.make(
            "pokemons.Pokemon", attack=20, defense=20, hit_points=55
        )  # higher hit_points

        # opponent's pokemons
        pokemon_4 = mommy.make("pokemons.Pokemon", attack=10, defense=10, hit_points=35)
        pokemon_5 = mommy.make("pokemons.Pokemon", attack=15, defense=15, hit_points=30)
        pokemon_6 = mommy.make("pokemons.Pokemon", attack=20, defense=20, hit_points=50)

        battle = mommy.make(
            "battles.Battle",
            creator=creator,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
            opponent_pokemon_1=pokemon_4,
            opponent_pokemon_2=pokemon_5,
            opponent_pokemon_3=pokemon_6,
        )

        winner = get_battle_result(battle)
        self.assertEqual(winner, battle.creator)

    def test_raises_exception_if_battle_has_not_been_resolved_when_getting_result(self):
        creator = mommy.make("users.User", email="creator@test.com")
        opponent = mommy.make("users.User", email="opponent@test.com")

        # creator's pokemons
        pokemon_1 = mommy.make("pokemons.Pokemon", attack=10, defense=10, hit_points=20)
        pokemon_2 = mommy.make("pokemons.Pokemon", attack=5, defense=5, hit_points=15)
        pokemon_3 = mommy.make("pokemons.Pokemon", attack=20, defense=20, hit_points=40)

        battle = mommy.make(
            "battles.Battle",
            creator=creator,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        with self.assertRaises(Exception):
            get_battle_result(battle)
