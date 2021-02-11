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
            "password1": "password",
            "password2": "password",
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
