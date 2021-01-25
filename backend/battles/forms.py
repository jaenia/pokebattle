from django import forms

from pokemons.exceptions import PokemonNotFound
from battles.models import Battle
from pokemons.helpers import save_pokemon, get_pokemons_points_sum
from pokemons.models import Pokemon
from pokemons.services import pokemon_exists
from users.models import User


class BattleForm(forms.ModelForm):
    creator = forms.ModelChoiceField(required=False, queryset=User.objects.all())

    """
    These input fields are used to get the Pokemons' ids in the form.
    We need to validate that selected Pokemons exist in PokeAPI before creating the battle.
    """
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

    def clean_creator_pokemon_1_input(self):
        data = self.cleaned_data.get("creator_pokemon_1_input")
        if not pokemon_exists(data):
            self.add_error("creator_pokemon_1_input", "Sorry, this pokemon was not found")
        return data

    def clean_creator_pokemon_2_input(self):
        data = self.cleaned_data.get("creator_pokemon_2_input")
        if not pokemon_exists(data):
            self.add_error("creator_pokemon_2_input", "Sorry, this pokemon was not found")
        return data

    def clean_creator_pokemon_3_input(self):
        data = self.cleaned_data.get("creator_pokemon_3_input")
        if not pokemon_exists(data):
            self.add_error("creator_pokemon_3_input", "Sorry, this pokemon was not found")
        return data

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["creator"] = self.fields["creator"].initial

        creator_pokemon_1_input = cleaned_data.get("creator_pokemon_1_input")
        creator_pokemon_2_input = cleaned_data.get("creator_pokemon_2_input")
        creator_pokemon_3_input = cleaned_data.get("creator_pokemon_3_input")

        pokemon_points_sum = 0
        try:
            pokemon_points_sum = get_pokemons_points_sum(
                [creator_pokemon_1_input, creator_pokemon_2_input, creator_pokemon_3_input]
            )
        except PokemonNotFound: # noqa #nosec
            pass

        if pokemon_points_sum > 600:
            raise forms.ValidationError("Pokemons' points sum cannot be more than 600")

        return cleaned_data

    def save(self, commit=True):
        self.instance.creator_pokemon_1 = save_pokemon(
            self.cleaned_data.get("creator_pokemon_1_input")
        )
        self.instance.creator_pokemon_2 = save_pokemon(
            self.cleaned_data.get("creator_pokemon_2_input")
        )
        self.instance.creator_pokemon_3 = save_pokemon(
            self.cleaned_data.get("creator_pokemon_3_input")
        )
        return super(BattleForm, self).save(commit)
