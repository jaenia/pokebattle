from django.test import TestCase, Client
from django.urls import reverse


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
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
