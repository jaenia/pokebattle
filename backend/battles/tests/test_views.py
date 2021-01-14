from django.test import TestCase, Client
from django.urls import reverse

from model_mommy import mommy

from battles.models import Battle


class BattleListViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_performance(self):
        mommy.make("battles.Battle")
        mommy.make("battles.Battle")

        url = reverse("battles:battle_list")

        with self.assertNumQueries(1):
            response = self.client.get(url)

        self.assertEqual(response.context["object_list"].count(), 2)

        mommy.make("battles.Battle")
        mommy.make("battles.Battle")

        with self.assertNumQueries(1):
            response = self.client.get(url)

        self.assertEqual(response.context["object_list"].count(), 4)

    def test_battle_list(self):
        battle1 = mommy.make("battles.Battle")
        battle2 = mommy.make("battles.Battle")

        url = reverse("battles:battle_list")
        response = self.client.get(url)

        self.assertContains(response, battle1.id, status_code=200)
        self.assertContains(response, battle2.id, status_code=200)


class BattleDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_battle_detail(self):
        battle = mommy.make("battles.Battle")

        url = reverse("battles:battle_detail", args=[battle.id])
        response = self.client.get(url)

        self.assertContains(response, battle.id, status_code=200)


class BattleCreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_battle_create(self):
        mommy.make("users.User")
        opponent = mommy.make("users.User")

        pokemon1 = mommy.make("pokemons.Pokemon", poke_id=1)
        pokemon2 = mommy.make("pokemons.Pokemon", poke_id=2)
        pokemon3 = mommy.make("pokemons.Pokemon", poke_id=3)

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1_input": pokemon1.id,
            "creator_pokemon_2_input": pokemon2.id,
            "creator_pokemon_3_input": pokemon3.id,
        }
        url = reverse("battles:battle_create")

        battle = Battle.objects.filter(opponent=opponent).first()
        self.assertIsNone(battle)

        response = self.client.post(url, data)

        battle = Battle.objects.filter(opponent=opponent).first()
        self.assertEqual(battle.opponent, opponent)

        self.assertEqual(response.status_code, 302)

    def test_cannot_create_battle_with_same_user_as_opponent_and_creator(self):
        current_user = mommy.make("users.User")

        pokemon1 = mommy.make("pokemons.Pokemon", poke_id=1)
        pokemon2 = mommy.make("pokemons.Pokemon", poke_id=2)
        pokemon3 = mommy.make("pokemons.Pokemon", poke_id=3)

        data = {
            "opponent": current_user.id,
            "creator_pokemon_1_input": pokemon1.id,
            "creator_pokemon_2_input": pokemon2.id,
            "creator_pokemon_3_input": pokemon3.id,
        }
        url = reverse("battles:battle_create")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
