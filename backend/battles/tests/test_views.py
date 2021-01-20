import responses

from django.test import TestCase, Client
from django.urls import reverse

from model_mommy import mommy

from battles.models import Battle
from common.constants import POKEAPI_BASE_URL


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

    @responses.activate
    def test_battle_create(self):
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

        mommy.make("users.User")
        opponent = mommy.make("users.User")

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1_input": 1,
            "creator_pokemon_2_input": 2,
            "creator_pokemon_3_input": 3,
        }
        url = reverse("battles:battle_create")

        battle = Battle.objects.filter(opponent=opponent).first()
        self.assertIsNone(battle)

        response = self.client.post(url, data)

        battle = Battle.objects.filter(opponent=opponent).first()
        self.assertEqual(battle.opponent, opponent)

        self.assertEqual(response.status_code, 302)

    @responses.activate
    def test_cannot_create_battle_with_same_user_as_opponent_and_creator(self):
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
        url = reverse("battles:battle_create")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
