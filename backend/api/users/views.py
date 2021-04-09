from django.shortcuts import render, redirect  # noqa
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from api.users.serializers import AuthTokenSerializer
from users.models import User


class LoginEndpoint(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserListEndpoint(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
