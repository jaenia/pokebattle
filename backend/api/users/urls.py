from django.urls import path

from . import views

urlpatterns = [
    path("token", views.LoginEndpoint.as_view(), name="token"),
]
