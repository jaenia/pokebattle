from django.test import TestCase
from model_mommy import mommy

from battles.helpers import get_battle_result


class BattleHelperTests(TestCase):
    def test_get_battle_result_without_draw(self):
        creator = mommy.make("users.User", email="creator@test.com")
        opponent = mommy.make("users.User", email="opponent@test.com")

        # creator's pokemons
        pokemon_1 = mommy.make("pokemons.Pokemon", attack=10, defense=10, hit_points=20)
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
        self.assertEqual(winner, battle.opponent)

    def test_get_battle_result_with_draw(self):
        creator = mommy.make("users.User", email="creator@test.com")
        opponent = mommy.make("users.User", email="opponent@test.com")

        # creator's pokemons
        pokemon_1 = mommy.make("pokemons.Pokemon", attack=10, defense=10, hit_points=20)
        pokemon_2 = mommy.make("pokemons.Pokemon", attack=15, defense=15, hit_points=40)
        pokemon_3 = mommy.make("pokemons.Pokemon", attack=20, defense=20, hit_points=55)

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
