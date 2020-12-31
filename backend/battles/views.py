from django.views.generic import CreateView, DetailView, ListView

from battles.forms import BattleForm
from battles.models import Battle
from users.models import User


class BattleCreate(CreateView):
    template_name = 'battles/battle_form.html'
    form_class = BattleForm

    def get_form_kwargs(self):
        kwargs = super(BattleCreate, self).get_form_kwargs()
        kwargs['user'] = User.objects.first()
        return kwargs


class BattleDetail(DetailView):
    model = Battle


class BattleList(ListView):
    model = Battle
