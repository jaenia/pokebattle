# Generated by Django 2.2.17 on 2020-12-30 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poke_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('attack', models.IntegerField()),
                ('defense', models.IntegerField()),
                ('hit_points', models.IntegerField()),
            ],
        ),
    ]
