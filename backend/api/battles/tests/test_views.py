import responses
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIClient

from battles.models import Battle
from common.constants import POKEAPI_BASE_URL


class PublicBattleListCreateEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        url = reverse("api_battles:battle_list_create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PrivateBattleListCreateEndpointTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test@test.com", "password123")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    @responses.activate
    def test_create_battle_successful(self):
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
            "creator": self.user.id,
            "opponent": opponent.id,
            "creator_pokemon_1": pokemon_1.name,
            "creator_pokemon_2": pokemon_2.name,
            "creator_pokemon_3": pokemon_3.name,
        }
        url = reverse("api_battles:battle_list_create")

        battle = Battle.objects.filter(opponent=opponent).first()
        self.assertIsNone(battle)

        response = self.client.post(url, data)

        battle = Battle.objects.filter(opponent=opponent).first()
        self.assertEqual(battle.opponent, opponent)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_battle_without_pokemons(self):
        opponent = mommy.make("users.User")

        data = {
            "creator": self.user.id,
            "opponent": opponent.id,
        }
        url = reverse("api_battles:battle_list_create")

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @responses.activate
    def test_cannot_create_battle_with_unexisting_pokemons(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon1", status=404)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon2", status=404)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon3", status=404)

        opponent = mommy.make("users.User")

        data = {
            "creator": self.user.id,
            "opponent": opponent.id,
            "creator_pokemon_1": "pokemon1",
            "creator_pokemon_2": "pokemon2",
            "creator_pokemon_3": "pokemon3",
        }
        url = reverse("api_battles:battle_list_create")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "creator_pokemon_1": ["Sorry, this pokemon was not found"],
                "creator_pokemon_2": ["Sorry, this pokemon was not found"],
                "creator_pokemon_3": ["Sorry, this pokemon was not found"],
            },
        )

    @responses.activate
    def test_cannot_create_battle_if_pokemon_points_sum_is_more_than_600(self):
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

        opponent = mommy.make("users.User")

        data = {
            "creator": self.user.id,
            "opponent": opponent.id,
            "creator_pokemon_1": pokemon_1.name,
            "creator_pokemon_2": pokemon_2.name,
            "creator_pokemon_3": pokemon_3.name,
        }
        url = reverse("api_battles:battle_list_create")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content,
            b'{"non_field_errors":["Pokemons\' points sum cannot be more than 600"]}',
        )


class PublicBattleRetrieveUpdateEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        url = reverse("api_battles:battle_retrieve_update", args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PrivateBattleRetrieveUpdateEndpointTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test@test.com", "password123")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    @responses.activate
    def test_opponent_select_pokemons(self):
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

        battle = mommy.make(
            "battles.Battle",
            creator=mommy.make("users.User"),
            opponent=self.user,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        data = {
            "creator": battle.creator.id,
            "opponent": battle.opponent.id,
            "creator_pokemon_1": battle.creator_pokemon_1,
            "creator_pokemon_2": battle.creator_pokemon_2,
            "creator_pokemon_3": battle.creator_pokemon_3,
            "opponent_pokemon_1": "pokemon3",
            "opponent_pokemon_2": "pokemon2",
            "opponent_pokemon_3": "pokemon1",
        }

        self.assertIsNone(battle.opponent_pokemon_1)
        self.assertIsNone(battle.opponent_pokemon_2)
        self.assertIsNone(battle.opponent_pokemon_3)

        url = reverse("api_battles:battle_retrieve_update", args=[battle.id])
        response = self.client.put(url, data)

        battle = Battle.objects.get(pk=battle.id)
        self.assertEqual(battle.opponent_pokemon_1.poke_id, 3)
        self.assertEqual(battle.opponent_pokemon_2.poke_id, 2)
        self.assertEqual(battle.opponent_pokemon_3.poke_id, 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_cannot_update_battle_with_unexisting_pokemons(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon3", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon4", status=404)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon5", status=404)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon6", status=404)

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

        battle = mommy.make(
            "battles.Battle",
            creator=mommy.make("users.User"),
            opponent=self.user,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        data = {
            "creator": battle.creator.id,
            "opponent": battle.opponent.id,
            "creator_pokemon_1": battle.creator_pokemon_1,
            "creator_pokemon_2": battle.creator_pokemon_2,
            "creator_pokemon_3": battle.creator_pokemon_3,
            "opponent_pokemon_1": "pokemon4",
            "opponent_pokemon_2": "pokemon5",
            "opponent_pokemon_3": "pokemon6",
        }

        url = reverse("api_battles:battle_retrieve_update", args=[battle.id])
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "opponent_pokemon_1": ["Sorry, this pokemon was not found"],
                "opponent_pokemon_2": ["Sorry, this pokemon was not found"],
                "opponent_pokemon_3": ["Sorry, this pokemon was not found"],
            },
        )

    @responses.activate
    def test_cannot_update_battle_if_pokemon_points_sum_is_more_than_600(self):
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon1", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon2", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon3", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon4", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon5", status=200)
        responses.add(responses.HEAD, f"{POKEAPI_BASE_URL}pokemon/pokemon6", status=200)

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
        mommy.make(
            "pokemons.Pokemon",
            poke_id=4,
            name="pokemon4",
            attack=100,
            defense=100,
            hit_points=100,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/4.png",
        )
        mommy.make(
            "pokemons.Pokemon",
            poke_id=5,
            name="pokemon5",
            attack=100,
            defense=100,
            hit_points=100,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/5.png",
        )
        mommy.make(
            "pokemons.Pokemon",
            poke_id=6,
            name="pokemon6",
            attack=100,
            defense=100,
            hit_points=100,
            image="https://raw.githubusercontent.com/"
            "PokeAPI/sprites/master/sprites/pokemon/6.png",
        )

        battle = mommy.make(
            "battles.Battle",
            creator=mommy.make("users.User"),
            opponent=self.user,
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        data = {
            "creator": battle.creator.id,
            "opponent": battle.opponent.id,
            "creator_pokemon_1": battle.creator_pokemon_1,
            "creator_pokemon_2": battle.creator_pokemon_2,
            "creator_pokemon_3": battle.creator_pokemon_3,
            "opponent_pokemon_1": "pokemon4",
            "opponent_pokemon_2": "pokemon5",
            "opponent_pokemon_3": "pokemon6",
        }

        url = reverse("api_battles:battle_retrieve_update", args=[battle.id])
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content,
            b'{"non_field_errors":["Pokemons\' points sum cannot be more than 600"]}',
        )

    @responses.activate
    def test_cannot_select_opponent_pokemons_if_user_is_not_opponent(self):
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

        battle = mommy.make(
            "battles.Battle",
            creator=mommy.make("users.User"),
            opponent=mommy.make("users.User"),
            creator_pokemon_1=pokemon_1,
            creator_pokemon_2=pokemon_2,
            creator_pokemon_3=pokemon_3,
        )

        data = {
            "creator": battle.creator.id,
            "opponent": battle.opponent.id,
            "creator_pokemon_1": battle.creator_pokemon_1,
            "creator_pokemon_2": battle.creator_pokemon_2,
            "creator_pokemon_3": battle.creator_pokemon_3,
            "opponent_pokemon_1": pokemon_3,
            "opponent_pokemon_2": pokemon_2,
            "opponent_pokemon_3": pokemon_1,
        }

        url = reverse("api_battles:battle_retrieve_update", args=[battle.id])
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content,
            b'{"non_field_errors":['
            b'"You can\'t update opponent Pokemons if you aren\'t the battle opponent"]}',
        )
