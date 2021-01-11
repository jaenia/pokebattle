# Generated by Django 2.2.17 on 2021-01-04 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('battles', '0003_battle_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battle_as_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='battle',
            name='opponent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battle_as_opponent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BattleTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battleteam_battle', to='battles.Battle')),
                ('pokemon_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battleteam_as_pokemon_1', to='pokemons.Pokemon')),
                ('pokemon_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battleteam_as_pokemon_2', to='pokemons.Pokemon')),
                ('pokemon_3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battleteam_as_pokemon_3', to='pokemons.Pokemon')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battleteam_as_trainer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]