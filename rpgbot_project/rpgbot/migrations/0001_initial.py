# Generated by Django 4.2.2 on 2023-07-12 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_type', models.CharField(choices=[('Warrior', 'Warrior'), ('Rogue', 'Rogue'), ('Mage', 'Mage')], max_length=50, verbose_name='class_type')),
                ('image', models.ImageField(blank=True, null=True, upload_to='class_images', verbose_name='image')),
                ('health', models.IntegerField(default=0, verbose_name='health')),
                ('attack', models.IntegerField(default=0, verbose_name='attack')),
                ('defense', models.IntegerField(default=0, verbose_name='defense')),
            ],
            options={
                'verbose_name': 'characterClass',
                'verbose_name_plural': 'characterClasss',
            },
        ),
        migrations.CreateModel(
            name='Enemy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('max_health', models.IntegerField(default=0, verbose_name='max_health')),
                ('current_health', models.IntegerField(default=0, verbose_name='current_health')),
                ('attack', models.IntegerField(default=0, verbose_name='attack')),
                ('defense', models.IntegerField(default=0, verbose_name='defense')),
                ('image', models.ImageField(blank=True, null=True, upload_to='enemy_images', verbose_name='image')),
                ('level', models.IntegerField(default=1, verbose_name='level')),
                ('gold', models.IntegerField(default=0, verbose_name='gold')),
                ('xp', models.IntegerField(default=10, verbose_name='experience')),
            ],
            options={
                'verbose_name': 'enemy',
                'verbose_name_plural': 'enemies',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('type', models.CharField(choices=[('Weapon', 'Weapon'), ('Body Armor', 'Body Armor'), ('Helmet', 'Helmet'), ('Leg Armor', 'Leg Armor'), ('Ring', 'Ring'), ('Amulet', 'Amulet'), ('Misc', 'Misc')], max_length=50, verbose_name='type')),
                ('attack', models.IntegerField(default=0, verbose_name='attack')),
                ('defense', models.IntegerField(default=0, verbose_name='defense')),
                ('health', models.IntegerField(default=0, verbose_name='health')),
                ('special_attributes', models.JSONField(blank=True, default=dict, null=True, verbose_name='speccial_attributes')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='name')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='description')),
                ('victory_message', models.CharField(blank=True, max_length=2000, null=True, verbose_name='victory_message')),
                ('defeat_message', models.CharField(blank=True, max_length=2000, null=True, verbose_name='defeat_message')),
                ('enemy', models.ManyToManyField(blank=True, to='rpgbot.enemy', verbose_name='enemies')),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='player ID')),
                ('discord_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='discord_name')),
                ('username', models.CharField(max_length=50, verbose_name='username')),
                ('money', models.IntegerField(default=0, verbose_name='money')),
                ('max_health', models.IntegerField(default=1, verbose_name='max_health')),
                ('current_health', models.IntegerField(default=1, verbose_name='current_health')),
                ('attack', models.IntegerField(default=0, verbose_name='attack')),
                ('defense', models.IntegerField(default=0, verbose_name='defense')),
                ('level', models.IntegerField(default=1, verbose_name='level')),
                ('xp', models.IntegerField(default=0, verbose_name='experience')),
                ('character_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='character_class', to='rpgbot.characterclass', verbose_name='Character class')),
                ('equipped_amulet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipped_amulet', to='rpgbot.item', verbose_name='equipped_amulet')),
                ('equipped_body_armour', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipped_body_armour', to='rpgbot.item', verbose_name='equipped_body_armour')),
                ('equipped_helmet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipped_helmet', to='rpgbot.item', verbose_name='equipped_helmet')),
                ('equipped_leg_armor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipped_leg_armor', to='rpgbot.item', verbose_name='equipped_leg_armor')),
                ('equipped_ring1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipped_ring1', to='rpgbot.item', verbose_name='equipped_ring1')),
                ('equipped_ring2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipped_ring2', to='rpgbot.item', verbose_name='equipped_ring2')),
                ('equipped_weapon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipped_weapon', to='rpgbot.item', verbose_name='equipped_weapon')),
                ('inventory', models.ManyToManyField(blank=True, null=True, related_name='inventory', to='rpgbot.item', verbose_name='inventory')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='rpgbot.location', verbose_name='location')),
            ],
            options={
                'verbose_name': 'player',
                'verbose_name_plural': 'players',
            },
        ),
        migrations.CreateModel(
            name='EnemyInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_health', models.IntegerField(default=0, verbose_name='current_health')),
                ('enemy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enemy_instances', to='rpgbot.enemy', verbose_name='enemy')),
            ],
            options={
                'verbose_name': 'enemyInstances',
                'verbose_name_plural': 'enemyInstancess',
            },
        ),
        migrations.AddField(
            model_name='enemy',
            name='drops',
            field=models.ManyToManyField(blank=True, related_name='drops', to='rpgbot.item', verbose_name='drops'),
        ),
    ]
