from django.test import TestCase
from model_mommy import mommy

from battles.models import Battle


class BattleQuerySetTests(TestCase):

    def test_get_settled_battles(self):
        creator = mommy.make("users.User")
        opponent = mommy.make("users.User")

        pokemon_1 = mommy.make("pokemons.Pokemon")
        pokemon_2 = mommy.make("pokemons.Pokemon")
        pokemon_3 = mommy.make("pokemons.Pokemon")

        battle_1 = mommy.make(
            "battles.Battle",
            creator=creator,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        battle_2 = mommy.make(
            "battles.Battle",
            creator=creator,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
            opponent_pokemon_1=pokemon_3,
            opponent_pokemon_2=pokemon_2,
            opponent_pokemon_3=pokemon_1,
        )

        battles = Battle.objects.settled()
        self.assertIn(battle_2, battles)
        self.assertNotIn(battle_1, battles)

    def test_get_ongoing_battles(self):
        creator = mommy.make("users.User")
        opponent = mommy.make("users.User")

        pokemon_1 = mommy.make("pokemons.Pokemon")
        pokemon_2 = mommy.make("pokemons.Pokemon")
        pokemon_3 = mommy.make("pokemons.Pokemon")

        battle_1 = mommy.make(
            "battles.Battle",
            creator=creator,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        battle_2 = mommy.make(
            "battles.Battle",
            creator=creator,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
            opponent_pokemon_1=pokemon_3,
            opponent_pokemon_2=pokemon_2,
            opponent_pokemon_3=pokemon_1,
        )

        battles = Battle.objects.ongoing()
        self.assertIn(battle_1, battles)
        self.assertNotIn(battle_2, battles)
