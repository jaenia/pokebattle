from django.test import TestCase

from users.forms import SignUpForm


class SignUpFormTests(TestCase):

    def test_create_user(self):
        data = {
            "email": "test@test.com",
            "password": "password",
        }

        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.email, "test@test.com")
