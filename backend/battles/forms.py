from django import forms

from battles.models import Battle
from users.models import User


class BattleForm(forms.ModelForm):
    creator = forms.ModelChoiceField(required=False, queryset=User.objects.all())

    class Meta:
        model = Battle
        fields = [
            "creator",
            "opponent",
            "creator_pokemon_1",
            "creator_pokemon_2",
            "creator_pokemon_3",
            "opponent_pokemon_1",
            "opponent_pokemon_2",
            "opponent_pokemon_3"
        ]

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user")
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(email=self.current_user.email)
        self.fields["creator"].initial = self.current_user

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["creator"] = self.fields["creator"].initial

        return cleaned_data
