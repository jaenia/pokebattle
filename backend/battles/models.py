from django.db import models
from django.urls import reverse

from users.models import User


class Battle(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="battle_as_creator",
    )
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="battle_as_opponent")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return reverse("battles:battle_detail", kwargs={"pk": self.pk})
