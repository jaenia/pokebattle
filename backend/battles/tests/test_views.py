from unittest import mock

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
        self.assertRedirects(
            response, reverse("battles:battle_update_opponent_pokemons", args=[battle.pk])
        )

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


class BattleUpdateOpponentPokemonsViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @responses.activate
    @mock.patch("battles.views.send_battle_result")
    def test_opponent_select_pokemons(self, send_mock):
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

        creator = mommy.make("users.User")
        opponent = mommy.make("users.User")

        pokemon_1 = mommy.make("pokemons.Pokemon")
        pokemon_2 = mommy.make("pokemons.Pokemon")
        pokemon_3 = mommy.make("pokemons.Pokemon")

        battle = mommy.make(
            "battles.Battle",
            creator=creator,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        data = {
            "opponent_pokemon_1_input": 3,
            "opponent_pokemon_2_input": 2,
            "opponent_pokemon_3_input": 1,
        }

        self.assertIsNone(battle.opponent_pokemon_1)
        self.assertIsNone(battle.opponent_pokemon_2)
        self.assertIsNone(battle.opponent_pokemon_3)

        url = reverse("battles:battle_update_opponent_pokemons", args=[battle.id])
        response = self.client.post(url, data)

        battle = Battle.objects.get(pk=battle.id)
        self.assertEqual(battle.opponent_pokemon_1.poke_id, 3)
        self.assertEqual(battle.opponent_pokemon_2.poke_id, 2)
        self.assertEqual(battle.opponent_pokemon_3.poke_id, 1)

        send_mock.assert_called_with(battle)
        self.assertEqual(response.status_code, 302)


class SettledBattlesListViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_list_settled_battles(self):
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

        url = reverse("battles:settled_battles_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, f"Pokebattle {battle_1.id}")
        self.assertContains(response, f"Pokebattle {battle_2.id}")
