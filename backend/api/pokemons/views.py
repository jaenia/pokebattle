from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from pokemons.models import Pokemon


class PokemonListEndpoint(generics.ListAPIView):
    queryset = Pokemon.objects.all()
    permission_classes = (IsAuthenticated,)
