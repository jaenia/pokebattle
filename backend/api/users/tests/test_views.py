from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class LoginEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        data = {"email": "test@test.com", "password": "testpass"}
        user = create_user(**data)
        url = reverse("api_users:token")

        token = Token.objects.filter(user=user).first()
        self.assertIsNone(token)

        res = self.client.post(url, data)

        token = Token.objects.get(user=user)
        self.assertEqual(token.user, user)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(email="test@test.com", password="testpass")
        payload = {
            "email": "test@test.com",
            "password": "wrong",
        }
        url = reverse("api_users:token")
        res = self.client.post(url, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        payload = {
            "email": "test@test.com",
            "password": "wrong",
        }
        url = reverse("api_users:token")
        res = self.client.post(url, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        url = reverse("api_users:token")
        res = self.client.post(url, {"email": "one", "password": ""})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
