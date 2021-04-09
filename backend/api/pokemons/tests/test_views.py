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
