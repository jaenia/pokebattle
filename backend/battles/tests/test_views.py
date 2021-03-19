from unittest import mock

import responses

from django.test import TestCase, Client
from django.urls import reverse

from model_mommy import mommy

from battles.models import Battle
from common.constants import POKEAPI_BASE_URL
from users.models import User


class BattleListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="password123")
        self.client = Client()
        self.client.force_login(self.user)

    def test_performance(self):
        mommy.make("battles.Battle")
        mommy.make("battles.Battle")

        url = reverse("battles:battle_list")

        with self.assertNumQueries(3):
            response = self.client.get(url)

        self.assertEqual(response.context["object_list"].count(), 2)

        mommy.make("battles.Battle")
        mommy.make("battles.Battle")

        with self.assertNumQueries(3):
            response = self.client.get(url)

        self.assertEqual(response.context["object_list"].count(), 4)

    def test_battle_list(self):
        battle1 = mommy.make("battles.Battle")
        battle2 = mommy.make("battles.Battle")

        url = reverse("battles:battle_list")
        response = self.client.get(url)

        self.assertContains(response, battle1.id, status_code=200)
        self.assertContains(response, battle2.id, status_code=200)

    def test_non_logged_user_cannot_access_battle_list(self):
        url = reverse("users:user_logout")
        self.client.get(url)

        url = reverse("battles:battle_list")
        response = self.client.get(url)

        self.assertRedirects(
            response, f"{reverse('users:user_login')}?next={reverse('battles:battle_list')}"
        )


class BattleDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="password123")
        self.client = Client()
        self.client.force_login(self.user)

    def test_battle_detail(self):
        battle = mommy.make("battles.Battle")

        url = reverse("battles:battle_detail", args=[battle.id])
        response = self.client.get(url)

        self.assertContains(response, battle.id, status_code=200)

    def test_non_logged_user_cannot_access_battle_detail(self):
        url = reverse("users:user_logout")
        self.client.get(url)

        battle = mommy.make("battles.Battle")
        url = reverse("battles:battle_detail", args=[battle.id])
        response = self.client.get(url)

        self.assertRedirects(
            response,
            f"{reverse('users:user_login')}?next="
            f"{reverse('battles:battle_detail', args=[battle.id])}",
        )

    def test_settled_battle_details_show_result(self):
        opponent = mommy.make("users.User")

        pokemon_1 = mommy.make("pokemons.Pokemon")
        pokemon_2 = mommy.make("pokemons.Pokemon")
        pokemon_3 = mommy.make("pokemons.Pokemon")

        battle = mommy.make(
            "battles.Battle",
            creator=self.user,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
            opponent_pokemon_1=pokemon_3,
            opponent_pokemon_2=pokemon_2,
            opponent_pokemon_3=pokemon_1,
        )

        url = reverse("battles:battle_detail", args=[battle.id])
        response = self.client.get(url)

        self.assertEqual(response.context_data["object"].winner, battle.winner)


class BattleCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="password123")
        self.client = Client()
        self.client.force_login(self.user)

    @responses.activate
    def test_battle_create(self):
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

        opponent = mommy.make("users.User")

        data = {
            "opponent": opponent.id,
            "creator_pokemon_1": pokemon_1.id,
            "creator_pokemon_2": pokemon_2.id,
            "creator_pokemon_3": pokemon_3.id,
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

        data = {
            "opponent": self.user.id,
            "creator_pokemon_1": pokemon_1.id,
            "creator_pokemon_2": pokemon_2.id,
            "creator_pokemon_3": pokemon_3.id,
        }
        url = reverse("battles:battle_create")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

    def test_non_logged_user_cannot_access_battle_creation(self):
        url = reverse("users:user_logout")
        self.client.get(url)

        url = reverse("battles:battle_create")
        response = self.client.get(url)

        self.assertRedirects(
            response, f"{reverse('users:user_login')}?next={reverse('battles:battle_create')}"
        )


class BattleUpdateOpponentPokemonsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="password123")
        self.client = Client()
        self.client.force_login(self.user)

    @responses.activate
    @mock.patch("battles.views.send_battle_result")
    def test_opponent_select_pokemons(self, send_mock):
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

        opponent = mommy.make("users.User")

        battle = mommy.make(
            "battles.Battle",
            creator=self.user,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        data = {
            "opponent_pokemon_1": pokemon_3.id,
            "opponent_pokemon_2": pokemon_2.id,
            "opponent_pokemon_3": pokemon_1.id,
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

    def test_non_logged_user_cannot_access_add_opponent_pokemons_to_battle(self):
        url = reverse("users:user_logout")
        self.client.get(url)

        battle = mommy.make("battles.Battle")
        url = reverse("battles:battle_update_opponent_pokemons", args=[battle.id])
        response = self.client.get(url)

        self.assertRedirects(
            response,
            f"{reverse('users:user_login')}?next="
            f"{reverse('battles:battle_update_opponent_pokemons', args=[battle.id])}",
        )


class SettledBattlesListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="password123")
        self.client = Client()
        self.client.force_login(self.user)

    def test_list_settled_battles(self):
        opponent = mommy.make("users.User")

        pokemon_1 = mommy.make("pokemons.Pokemon")
        pokemon_2 = mommy.make("pokemons.Pokemon")
        pokemon_3 = mommy.make("pokemons.Pokemon")

        battle_1 = mommy.make(
            "battles.Battle",
            creator=self.user,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        battle_2 = mommy.make(
            "battles.Battle",
            creator=self.user,
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

        battles = response.context_data["object_list"]
        self.assertIn(battle_2, battles)
        self.assertNotIn(battle_1, battles)

    def test_non_logged_user_cannot_access_settled_battles_list(self):
        url = reverse("users:user_logout")
        self.client.get(url)

        url = reverse("battles:settled_battles_list")
        response = self.client.get(url)

        self.assertRedirects(
            response,
            f"{reverse('users:user_login')}?next={reverse('battles:settled_battles_list')}",
        )


class OngoingBattlesListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="password123")
        self.client = Client()
        self.client.force_login(self.user)

    def test_list_settled_battles(self):
        opponent = mommy.make("users.User")

        pokemon_1 = mommy.make("pokemons.Pokemon")
        pokemon_2 = mommy.make("pokemons.Pokemon")
        pokemon_3 = mommy.make("pokemons.Pokemon")

        battle_1 = mommy.make(
            "battles.Battle",
            creator=self.user,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        battle_2 = mommy.make(
            "battles.Battle",
            creator=self.user,
            opponent=opponent,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
            opponent_pokemon_1=pokemon_3,
            opponent_pokemon_2=pokemon_2,
            opponent_pokemon_3=pokemon_1,
        )

        url = reverse("battles:ongoing_battles_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        battles = response.context_data["object_list"]
        self.assertIn(battle_1, battles)
        self.assertNotIn(battle_2, battles)

    def test_non_logged_user_cannot_access_ongoing_battles_list(self):
        url = reverse("users:user_logout")
        self.client.get(url)

        url = reverse("battles:ongoing_battles_list")
        response = self.client.get(url)

        self.assertRedirects(
            response,
            f"{reverse('users:user_login')}?next={reverse('battles:ongoing_battles_list')}",
        )
