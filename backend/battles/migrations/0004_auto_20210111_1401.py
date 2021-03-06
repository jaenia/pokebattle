# Generated by Django 2.2.17 on 2021-01-11 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
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
    ]
