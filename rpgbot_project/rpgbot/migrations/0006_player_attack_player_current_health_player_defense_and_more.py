# Generated by Django 4.2.2 on 2023-06-29 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpgbot', '0005_characterclass_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='attack',
            field=models.IntegerField(default='0', verbose_name='attack'),
        ),
        migrations.AddField(
            model_name='player',
            name='current_health',
            field=models.IntegerField(default=1, verbose_name='current_health'),
        ),
        migrations.AddField(
            model_name='player',
            name='defense',
            field=models.IntegerField(default='0', verbose_name='defense'),
        ),
        migrations.AddField(
            model_name='player',
            name='max_health',
            field=models.IntegerField(default=1, verbose_name='max_health'),
        ),
        migrations.AddField(
            model_name='player',
            name='money',
            field=models.IntegerField(default=0, verbose_name='money'),
        ),
    ]