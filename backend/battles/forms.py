from django import forms
from django.core.exceptions import ValidationError

from battles.models import Battle
from pokemons.helpers import save_pokemon
from pokemons.models import Pokemon
from pokemons.services import pokemon_exists
from users.models import User


class BattleForm(forms.ModelForm):
    creator = forms.ModelChoiceField(required=False, queryset=User.objects.all())

    creator_pokemon_1_input = forms.IntegerField(required=True)
    creator_pokemon_2_input = forms.IntegerField(required=True)
    creator_pokemon_3_input = forms.IntegerField(required=True)

    creator_pokemon_1 = forms.ModelChoiceField(required=False, queryset=Pokemon.objects.all())
    creator_pokemon_2 = forms.ModelChoiceField(required=False, queryset=Pokemon.objects.all())
    creator_pokemon_3 = forms.ModelChoiceField(required=False, queryset=Pokemon.objects.all())

    class Meta:
        model = Battle
        fields = [
            "creator",
            "opponent",
            "creator_pokemon_1_input",
            "creator_pokemon_2_input",
            "creator_pokemon_3_input",
            "creator_pokemon_1",
            "creator_pokemon_2",
            "creator_pokemon_3",
        ]

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user")
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(email=self.current_user.email)
        self.fields["creator"].initial = self.current_user

    def clean_creator_pokemon_1(self):
        data = self.cleaned_data.get('creator_pokemon_1_input')
        if not pokemon_exists(data):
            raise ValidationError('Sorry, this pokemon was not found.')
        data = save_pokemon(data)
        return data

    def clean_creator_pokemon_2(self):
        data = self.cleaned_data.get('creator_pokemon_2_input')
        if not pokemon_exists(data):
            raise ValidationError('Sorry, this pokemon was not found.')
        data = save_pokemon(data)
        return data

    def clean_creator_pokemon_3(self):
        data = self.cleaned_data.get('creator_pokemon_3_input')
        if not pokemon_exists(data):
            raise ValidationError('Sorry, this pokemon was not found.')
        data = save_pokemon(data)
        return data

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["creator"] = self.fields["creator"].initial

        return cleaned_data
