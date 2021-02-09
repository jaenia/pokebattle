from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
