from django.db import models
from django.urls import reverse

from battles.helpers import get_battle_result
from pokemons.models import Pokemon
from users.models import User


class BattleQuerySet(models.QuerySet):
    def settled(self):
        return self.filter(
            opponent_pokemon_1__isnull=False,
            opponent_pokemon_2__isnull=False,
            opponent_pokemon_3__isnull=False,
        )


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
        blank=True,
        null=True,
    )
    creator_pokemon_2 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_creator_pokemon_2",
        blank=True,
        null=True,
    )
    creator_pokemon_3 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_creator_pokemon_3",
        blank=True,
        null=True,
    )

    opponent_pokemon_1 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_opponent_pokemon_1",
        blank=True,
        null=True,
    )
    opponent_pokemon_2 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_opponent_pokemon_2",
        blank=True,
        null=True,
    )
    opponent_pokemon_3 = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="battle_as_opponent_pokemon_3",
        blank=True,
        null=True,
    )

    objects = BattleQuerySet().as_manager()

    @property
    def winner(self):
        return get_battle_result(self)

    def __str__(self):
        return f"Battle #{self.id}: {self.creator.email} X {self.opponent.email}"

    def get_absolute_url(self):
        return reverse("battles:battle_detail", kwargs={"pk": self.pk})
