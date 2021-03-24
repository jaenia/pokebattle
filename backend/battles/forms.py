from dal import autocomplete

from django import forms

from battles.exceptions import DuplicatedPokemonPositions
from battles.helpers import position_pokemons
from battles.models import Battle
from pokemons.exceptions import PokemonNotFound
from pokemons.helpers import get_pokemons_points_sum
from pokemons.models import Pokemon
from pokemons.services import pokemon_exists
from users.models import User

POKEMON_POSITION_CHOICES = [
    (1, "Position 1"),
    (2, "Position 2"),
    (3, "Position 3"),
]


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

    position_creator_pokemon_1 = forms.ChoiceField(
        choices=POKEMON_POSITION_CHOICES, initial=1, required=False
    )
    position_creator_pokemon_2 = forms.ChoiceField(
        choices=POKEMON_POSITION_CHOICES, initial=2, required=False
    )
    position_creator_pokemon_3 = forms.ChoiceField(
        choices=POKEMON_POSITION_CHOICES, initial=3, required=False
    )

    class Meta:
        model = Battle
        fields = [
            "creator",
            "opponent",
            "creator_pokemon_1",
            "creator_pokemon_2",
            "creator_pokemon_3",
            "position_creator_pokemon_1",
            "position_creator_pokemon_2",
            "position_creator_pokemon_3",
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

        position_creator_pokemon_1 = cleaned_data.get("position_creator_pokemon_1")
        position_creator_pokemon_2 = cleaned_data.get("position_creator_pokemon_2")
        position_creator_pokemon_3 = cleaned_data.get("position_creator_pokemon_3")

        pokemon_points_sum = 0
        try:
            pokemon_points_sum = get_pokemons_points_sum(
                [creator_pokemon_1.name, creator_pokemon_2.name, creator_pokemon_3.name]
            )
        except PokemonNotFound:
            pass

        if pokemon_points_sum > 600:
            raise forms.ValidationError("Pokemons' points sum cannot be more than 600")

        # The exception treatment needs to be in clean method,
        # so it can show the Validation Error in the form
        try:
            position_pokemons(
                [creator_pokemon_1, creator_pokemon_2, creator_pokemon_3],
                [
                    position_creator_pokemon_1,
                    position_creator_pokemon_2,
                    position_creator_pokemon_3,
                ],
            )
        except DuplicatedPokemonPositions:
            raise forms.ValidationError("Please add each Pokemon in a different position")

        return cleaned_data

    def save(self, commit=True):
        creator_pokemon_1 = self.cleaned_data.get("creator_pokemon_1")
        creator_pokemon_2 = self.cleaned_data.get("creator_pokemon_2")
        creator_pokemon_3 = self.cleaned_data.get("creator_pokemon_3")

        position_creator_pokemon_1 = self.cleaned_data.get("position_creator_pokemon_1")
        position_creator_pokemon_2 = self.cleaned_data.get("position_creator_pokemon_2")
        position_creator_pokemon_3 = self.cleaned_data.get("position_creator_pokemon_3")

        positioned_pokemons = position_pokemons(
            [creator_pokemon_1, creator_pokemon_2, creator_pokemon_3],
            [position_creator_pokemon_1, position_creator_pokemon_2, position_creator_pokemon_3],
        )

        self.instance.creator_pokemon_1 = positioned_pokemons[0]
        self.instance.creator_pokemon_2 = positioned_pokemons[1]
        self.instance.creator_pokemon_3 = positioned_pokemons[2]

        return super(BattleForm, self).save(commit)


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
                [opponent_pokemon_1.name, opponent_pokemon_2.name, opponent_pokemon_3.name]
            )
        except PokemonNotFound:
            pass

        if pokemon_points_sum > 600:
            raise forms.ValidationError("Pokemons' points sum cannot be more than 600")

        return cleaned_data
