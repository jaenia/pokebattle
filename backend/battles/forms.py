from django import forms
from django.core.exceptions import ValidationError

from battles.models import Battle
from users.models import User


class BattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['creator', 'opponent']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields['opponent'].queryset = User.objects.exclude(email=user.email)

    def clean(self):
        cleaned_data = super().clean()
        creator = cleaned_data.get('creator')
        opponent = cleaned_data.get('opponent')

        self.cleaned_data['creator'] = User.objects.first()

        if creator == opponent:
            raise ValidationError('You can not be your own opponent. Please, choose someone else.')

        return cleaned_data
