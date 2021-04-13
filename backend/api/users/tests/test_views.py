from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
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


class PublicUserListEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        url = reverse("api_users:user_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PrivateUserListEndpointTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test@test.com", "password123")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_see_users_list(self):
        mommy.make("users.User", email="user1@test.com")
        mommy.make("users.User", email="user2@test.com")

        url = reverse("api_users:user_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"user1@test.com", response.content)
        self.assertIn(b"user2@test.com", response.content)
