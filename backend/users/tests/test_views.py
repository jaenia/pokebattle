from django.contrib import auth
from django.test import TestCase, Client
from django.urls import reverse

from users.models import User


class SignUpViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup(self):
        data = {
            "email": "test@test.com",
            "password": "password",
        }

        url = reverse("users:user_signup")

        user = User.objects.filter(email="test@test.com").first()
        self.assertIsNone(user)

        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("battles:battle_list"))

        user = User.objects.filter(email="test@test.com").first()
        self.assertEqual(user.email, "test@test.com")

        logged_user = auth.get_user(self.client)
        self.assertEqual(logged_user, user)


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_with_success(self):
        data = {"username": "test@test.com", "password": "password"}

        user = User.objects.create_user(email="test@test.com", password="password")

        url = reverse("users:user_login")
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("battles:battle_list"))

        logged_user = auth.get_user(self.client)
        self.assertEqual(logged_user, user)

    def test_login_with_wrong_password(self):
        data = {"username": "test@test.com", "password": "wrongpassword"}

        User.objects.create_user(email="test@test.com", password="password")

        url = reverse("users:user_login")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
