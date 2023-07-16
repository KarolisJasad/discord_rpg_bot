# Generated by Django 4.2.2 on 2023-07-16 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rpgbot', '0006_shop_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rpgbot.item')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rpgbot.player')),
            ],
        ),
    ]
