from django.contrib.auth import authenticate, login
from django.shortcuts import render  # noqa
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import SignUpForm


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("battles:battle_list")
    template_name = "auth/signup.html"

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get("email"), form.cleaned_data.get("password1")
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid
