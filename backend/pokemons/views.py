from dal import autocomplete

from pokemons.models import Pokemon


class PokemonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Pokemon.objects.none()

        qs = Pokemon.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
