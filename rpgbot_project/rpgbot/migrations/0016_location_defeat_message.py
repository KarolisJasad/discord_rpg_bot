# Generated by Django 4.2.2 on 2023-07-03 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpgbot', '0015_alter_location_victory_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='defeat_message',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='defeat_message'),
        ),
    ]