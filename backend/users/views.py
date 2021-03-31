from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect  # noqa
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import SignUpForm


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "auth/signup.html"

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(username=email, password=password)
        login(self.request, user)

        return valid

    def get_success_url(self):
        return reverse("battles:battle_list")


class Login(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True


class Logout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("users:user_login")
    login_url = reverse_lazy("users:user_login")

