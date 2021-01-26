from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from battles.forms import BattleForm, BattleOpponentPokemonsForm
from battles.models import Battle
from users.models import User


class BattleCreate(CreateView):
    template_name = "battles/battle_form.html"
    form_class = BattleForm

    def get_form_kwargs(self):
        kwargs = super(BattleCreate, self).get_form_kwargs()
        kwargs["current_user"] = User.objects.first()
        return kwargs

    def get_success_url(self):
        return reverse("battles:battle_update_opponent_pokemons", kwargs={"pk": self.object.pk})


class BattleUpdateOpponentPokemons(UpdateView):
    model = Battle
    form_class = BattleOpponentPokemonsForm
    template_name = "battles/battle_opponent_pokemons_form.html"


class BattleDetail(DetailView):
    model = Battle


class BattleList(ListView):
    model = Battle
