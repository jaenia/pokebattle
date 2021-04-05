from django.shortcuts import render, redirect  # noqa
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api.battles.serializers import BattleSerializer
from battles.models import Battle


class BattleListCreateEndpoint(generics.ListCreateAPIView):
    serializer_class = BattleSerializer
    queryset = Battle.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
