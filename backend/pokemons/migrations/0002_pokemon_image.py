# Generated by Django 2.2.19 on 2021-02-23 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='image',
            field=models.ImageField(blank=True, upload_to='pokemon_images/'),
        ),
    ]
