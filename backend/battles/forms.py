from dal import autocomplete

from django import forms

from battles.models import Battle
from pokemons.exceptions import PokemonNotFound
from pokemons.helpers import get_pokemons_points_sum
from pokemons.models import Pokemon
from pokemons.services import pokemon_exists
from users.models import User


class BattleForm(forms.ModelForm):
    creator = forms.ModelChoiceField(required=False, queryset=User.objects.all())

    creator_pokemon_1 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(url="pokemons:pokemon_autocomplete"),
    )
    creator_pokemon_2 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(url="pokemons:pokemon_autocomplete"),
    )
    creator_pokemon_3 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(url="pokemons:pokemon_autocomplete"),
    )

    class Meta:
        model = Battle
        fields = [
            "creator",
            "opponent",
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
        data = self.cleaned_data.get("creator_pokemon_1")
        if not pokemon_exists(data):
            self.add_error("creator_pokemon_1", "Sorry, this pokemon was not found")
        return data

    def clean_creator_pokemon_2(self):
        data = self.cleaned_data.get("creator_pokemon_2")
        if not pokemon_exists(data):
            self.add_error("creator_pokemon_2", "Sorry, this pokemon was not found")
        return data

    def clean_creator_pokemon_3(self):
        data = self.cleaned_data.get("creator_pokemon_3")
        if not pokemon_exists(data):
            self.add_error("creator_pokemon_3", "Sorry, this pokemon was not found")
        return data

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["creator"] = self.fields["creator"].initial

        creator_pokemon_1 = cleaned_data.get("creator_pokemon_1")
        creator_pokemon_2 = cleaned_data.get("creator_pokemon_2")
        creator_pokemon_3 = cleaned_data.get("creator_pokemon_3")

        pokemon_points_sum = 0
        try:
            pokemon_points_sum = get_pokemons_points_sum(
                [creator_pokemon_1, creator_pokemon_2, creator_pokemon_3]
            )
        except PokemonNotFound:
            pass

        if pokemon_points_sum > 600:
            raise forms.ValidationError("Pokemons' points sum cannot be more than 600")

        return cleaned_data


class BattleOpponentPokemonsForm(forms.ModelForm):
    opponent_pokemon_1 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(url="pokemons:pokemon_autocomplete"),
    )
    opponent_pokemon_2 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(url="pokemons:pokemon_autocomplete"),
    )
    opponent_pokemon_3 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(url="pokemons:pokemon_autocomplete"),
    )

    class Meta:
        model = Battle
        fields = [
            "opponent_pokemon_1",
            "opponent_pokemon_2",
            "opponent_pokemon_3",
        ]

    def clean_opponent_pokemon_1(self):
        data = self.cleaned_data.get("opponent_pokemon_1")
        if not pokemon_exists(data):
            self.add_error("opponent_pokemon_1", "Sorry, this pokemon was not found")
        return data

    def clean_opponent_pokemon_2(self):
        data = self.cleaned_data.get("opponent_pokemon_2")
        if not pokemon_exists(data):
            self.add_error("opponent_pokemon_2", "Sorry, this pokemon was not found")
        return data

    def clean_opponent_pokemon_3(self):
        data = self.cleaned_data.get("opponent_pokemon_3")
        if not pokemon_exists(data):
            self.add_error("opponent_pokemon_3", "Sorry, this pokemon was not found")
        return data

    def clean(self):
        cleaned_data = super().clean()

        opponent_pokemon_1 = cleaned_data.get("opponent_pokemon_1")
        opponent_pokemon_2 = cleaned_data.get("opponent_pokemon_2")
        opponent_pokemon_3 = cleaned_data.get("opponent_pokemon_3")

        pokemon_points_sum = 0
        try:
            pokemon_points_sum = get_pokemons_points_sum(
                [opponent_pokemon_1, opponent_pokemon_2, opponent_pokemon_3]
            )
        except PokemonNotFound:
            pass

        if pokemon_points_sum > 600:
            raise forms.ValidationError("Pokemons' points sum cannot be more than 600")

        return cleaned_data
