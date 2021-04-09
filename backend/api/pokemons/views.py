from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.pokemons.serializers import PokemonSerializer
from pokemons.models import Pokemon


class PokemonListEndpoint(generics.ListAPIView):
    serializer_class = PokemonSerializer
    queryset = Pokemon.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
