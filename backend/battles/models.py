from django.db import models
from django.urls import reverse

from pokemons.models import Pokemon
from users.models import User


class Battle(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="battle_as_creator",
    )
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battle_as_opponent")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    creator_pokemon_1 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_creator_pokemon_1",
    )
    creator_pokemon_2 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_creator_pokemon_2",
    )
    creator_pokemon_3 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_creator_pokemon_3",
    )

    opponent_pokemon_1 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_opponent_pokemon_1",
    )
    opponent_pokemon_2 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_opponent_pokemon_2",
    )
    opponent_pokemon_3 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_opponent_pokemon_3",
    )

    def __str__(self):
        return f"Battle #{self.id}: {self.creator.email} X {self.opponent.email}"

    def get_absolute_url(self):
        return reverse("battles:battle_detail", kwargs={"pk": self.pk})
