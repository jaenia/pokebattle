from django.shortcuts import render  # noqa
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import SignUpForm


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("battles:battle_list")
    template_name = "auth/signup.html"
