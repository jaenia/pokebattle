from django.urls import path

from . import views

urlpatterns = [
    path("token", views.LoginEndpoint.as_view(), name="token"),
    path("", views.UserListEndpoint.as_view(), name="user_list"),
]
