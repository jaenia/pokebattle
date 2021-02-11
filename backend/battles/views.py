from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from battles.forms import BattleForm, BattleOpponentPokemonsForm
from battles.helpers import send_battle_result
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

    def post(self, request, *args, **kwargs):
        super(BattleUpdateOpponentPokemons, self).post(request, *args, **kwargs)
        send_battle_result(self.get_object())
        return redirect(self.get_success_url())


class BattleDetail(DetailView):
    model = Battle


class BattleList(ListView):
    model = Battle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged_user'] = self.request.user
        return context


class SettledBattlesList(ListView):
    model = Battle
    template_name = "battles/battle_settled_list.html"

    def get_queryset(self):
        return Battle.objects.settled()


class OngoingBattlesList(ListView):
    model = Battle
    template_name = "battles/battle_ongoing_list.html"

    def get_queryset(self):
        return Battle.objects.ongoing()
