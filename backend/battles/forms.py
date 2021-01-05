from django import forms
from django.core.exceptions import ValidationError

from battles.models import Battle
from users.models import User


class BattleForm(forms.ModelForm):
    creator = forms.ModelChoiceField(required=False, queryset=User.objects.all())

    class Meta:
        model = Battle
        fields = ['creator', 'opponent']

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields['opponent'].queryset = User.objects.exclude(email=self.current_user.email)
        self.fields['creator'].initial = self.current_user

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['creator'] = self.fields['creator'].initial

        return cleaned_data
