from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class PublicBattleListCreateEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        url = reverse("api_pokemons:pokemon_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PrivatePokemonListEndpointTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test@test.com", "password123")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_see_users_list(self):
        url = reverse("api_pokemons:pokemon_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
