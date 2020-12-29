from django.shortcuts import get_object_or_404
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

    def form_valid(self, form):
        creator = get_object_or_404(User, email='jaenia@vinta.com.br')
        form.instance.creator = creator
        return super().form_valid(form)


class BattleDetail(DetailView):
    model = Battle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BattleList(ListView):
    model = Battle
