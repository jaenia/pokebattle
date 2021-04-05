from django.urls import path

from . import views

urlpatterns = [
    path("token", views.CreateTokenEndpoint.as_view(), name="token"),
]
