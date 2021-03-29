from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("signup", views.SignUp.as_view(), name="user_signup"),
    path("login", views.Login.as_view(), name="user_login"),
    path("logout", views.Logout.as_view(), name="user_logout"),
    path("token", views.CreateTokenView.as_view(), name="token"),
]
