from django.db import models


class Pokemon(models.Model):
    poke_id = models.IntegerField()
    name = models.CharField(max_length=100)
    attack = models.IntegerField()
    defense = models.IntegerField()
    hit_points = models.IntegerField()
    image_url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
