# Generated by Django 4.2.2 on 2023-07-03 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpgbot', '0016_location_defeat_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='enemy',
            name='gold',
            field=models.IntegerField(default=0, verbose_name='gold'),
        ),
    ]