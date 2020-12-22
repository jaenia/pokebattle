from django import forms

from battles.models import Battle
from users.models import User


class BattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['opponent']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields['opponent'].queryset = User.objects.exclude(email=user.email)
