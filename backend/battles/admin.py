from django.contrib import admin

from battles.models import Battle, BattleTeam

admin.site.register(Battle, BattleTeam)
