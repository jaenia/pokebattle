# Generated by Django 2.2.17 on 2020-12-22 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0002_auto_20201222_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
