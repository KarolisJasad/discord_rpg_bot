from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import random
from asgiref.sync import sync_to_async
from django.contrib.postgres.fields import JSONField
import discord
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

CHARACTER_CLASSES = [
    ("Warrior", "Warrior"),
    ("Rogue", "Rogue"),
    ("Mage", "Mage")    
]

class Player(models.Model):
    player_id = models.CharField(_("player ID"), max_length=50, primary_key=True)
    discord_name = models.CharField(_("discord_name"), max_length=50, blank=True, null=True)
    username = models.CharField(_("username"), max_length=50)
    money = models.IntegerField(_("money"), default=0)
    max_health = models.IntegerField(_("max_health"), default=1)
    current_health = models.IntegerField(_("current_health"), default=1)
    attack = models.IntegerField(_("attack"), default=0)
    defense = models.IntegerField(_("defense"), default=0)
    level = models.IntegerField(_("level"), default=1)
    xp = models.IntegerField(_("experience"), default=0)
    location = models.ForeignKey(
        "Location", 
        verbose_name=_("location"), 
        on_delete=models.CASCADE,
        related_name='location',
        blank=True,
        null=True
    )
    character_class = models.ForeignKey(
        "CharacterClass", 
        verbose_name=_("Character class"), 
        on_delete=models.CASCADE,
        related_name='character_class',
        blank=True,
        null=True,
    )
    inventory = models.ManyToManyField(
        "Item",
        verbose_name=_("inventory"),
        related_name="inventory",
        blank=True,
        null=True
    )
    equipped_weapon = models.ForeignKey(
        "Item",
        verbose_name=_("equipped_weapon"),
        on_delete=models.SET_NULL,
        related_name="equipped_weapon",
        blank=True,
        null=True
    )
    equipped_body_armour = models.ForeignKey(
        "Item",
        verbose_name=_("equipped_body_armour"),
        on_delete=models.SET_NULL,
        related_name="equipped_body_armour",
        blank=True,
        null=True
    )
    equipped_helmet = models.ForeignKey(
        "Item",
        verbose_name=_("equipped_helmet"),
        on_delete=models.SET_NULL,
        related_name="equipped_helmet",
        blank=True,
        null=True
    )
    equipped_leg_armor = models.ForeignKey(
        "Item",
        verbose_name=_("equipped_leg_armor"),
        on_delete=models.SET_NULL,
        related_name="equipped_leg_armor",
        blank=True,
        null=True
    )
    equipped_ring1 = models.ForeignKey(
        "Item",
        verbose_name=_("equipped_ring1"),
        on_delete=models.SET_NULL,
        related_name="equipped_ring1",
        blank=True,
        null=True
    )
    equipped_ring2 = models.ForeignKey(
        "Item",
        verbose_name=_("equipped_ring2"),
        on_delete=models.SET_NULL,
        related_name="equipped_ring2",
        blank=True,
        null=True
    )
    equipped_amulet = models.ForeignKey(
        "Item",
        verbose_name=_("equipped_amulet"),
        on_delete=models.SET_NULL,
        related_name="equipped_amulet",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("player")
        verbose_name_plural = _("players")

    def can_equip_item(self, item):
        # Check if the player can equip the item based on the item's type
        item_type = item.type.lower()
        weapon = Item.WEAPON.lower()
        body_armor = Item.BODY_ARMOR.lower()
        leg_armor = Item.LEG_ARMOR.lower()
        helmet = Item.HELMET.lower()
        ring = Item.RING.lower()
        amulet = Item.AMULET.lower()
        if item_type == weapon:
            return True
        elif item_type == body_armor:
            return True
        elif item_type == helmet:
            return True
        elif item_type == leg_armor:
            return True
        elif item_type == ring:
            if self.equipped_ring1 and self.equipped_ring2:
                return True
            elif not self.equipped_ring1:
                return True
            elif not self.equipped_ring2:
                return True
        elif item_type == amulet:
            return True
        else:
            return False

    def equip_item(self, item):
        # Equip the item based on its type
        if item.type == Item.WEAPON:
            if self.equipped_weapon:
                # Put the currently equipped weapon in the inventory
                self.attack -= self.equipped_weapon.attack
                self.inventory.add(self.equipped_weapon)
            self.equipped_weapon = item
            self.attack += self.equipped_weapon.attack
        elif item.type == Item.BODY_ARMOR:
            if self.equipped_body_armour:
                # Put the currently equipped body armor in the inventory
                self.defense -= self.equipped_body_armour.defense
                self.max_health -= self.equipped_body_armour.health
                if self.current_health > self.max_health:
                    self.current_health == self.max_health
                self.inventory.add(self.equipped_body_armour)
            self.equipped_body_armour = item
            self.defense += self.equipped_body_armour.defense
            self.max_health += self.equipped_body_armour.health
            self.current_health += self.equipped_body_armour.health
        elif item.type == Item.HELMET:
            if self.equipped_helmet:
                # Put the currently equipped helmet in the inventory
                self.defense -= self.equipped_helmet.defense
                self.max_health -= self.equipped_helmet.health
                if self.current_health > self.max_health:
                    self.current_health == self.max_health
                self.inventory.add(self.equipped_helmet)
            self.equipped_helmet = item
            self.defense += self.equipped_helmet.defense
            self.max_health += self.equipped_helmet.health
            self.current_health += self.equipped_helmet.health
        elif item.type == Item.LEG_ARMOR:
            if self.equipped_leg_armor:
                self.defense -= self.equipped_leg_armor.defense
                self.max_health -= self.equipped_leg_armor.health
                if self.current_health > self.max_health:
                    self.current_health == self.max_health
                self.inventory.add(self.equipped_leg_armor)
            self.equipped_leg_armor = item
            self.defense += self.equipped_leg_armor.defense
            self.max_health += self.equipped_leg_armor.health
            self.current_health += self.equipped_leg_armor.health
        elif item.type == Item.RING:
            if not self.equipped_ring1:
                self.equipped_ring1 = item
                self.attack += self.equipped_ring1.attack
                self.defense += self.equipped_ring1.defense
                self.max_health += self.equipped_ring1.health
                self.current_health += self.equipped_ring1.health
            elif not self.equipped_ring2:
                self.equipped_ring2 = item
                self.attack += self.equipped_ring2.attack
                self.defense += self.equipped_ring2.defense
                self.max_health += self.equipped_ring2.health
                self.current_health += self.equipped_ring2.health
            else:
                # Replace the ring with the lowest attack value
                if self.equipped_ring1.attack <= self.equipped_ring2.attack:
                    self.inventory.add(self.equipped_ring1)
                    self.attack -= self.equipped_ring1.attack
                    self.defense -= self.equipped_ring1.defense
                    self.max_health -= self.equipped_ring1.health
                    if self.current_health > self.max_health:
                        self.current_health == self.max_health
                    self.equipped_ring1 = item
                    self.attack += self.equipped_ring1.attack
                    self.defense += self.equipped_ring1.defense
                    self.max_health += self.equipped_ring1.health
                    self.current_health += self.equipped_ring1.health
                else:
                    self.inventory.add(self.equipped_ring2)
                    self.attack -= self.equipped_ring2.attack
                    self.defense -= self.equipped_ring2.defense
                    self.max_health -= self.equipped_ring2.health
                    if self.current_health > self.max_health:
                        self.current_health == self.max_health
                    self.equipped_ring2 = item
                    self.attack += self.equipped_ring2.attack
                    self.defense += self.equipped_ring2.defense
                    self.max_health += self.equipped_ring2.health
                    self.current_health += self.equipped_ring2.health
        elif item.type == Item.AMULET:
            if self.equipped_amulet:
                # Put the currently equipped amulet in the inventory
                self.inventory.add(self.equipped_amulet)
                self.attack -= self.equipped_amulet.attack
                self.defense -= self.equipped_amulet.defense
                self.max_health -= self.equipped_amulet.health
                if self.current_health > self.max_health:
                    self.current_health == self.max_health
            self.equipped_amulet = item
            self.attack += self.equipped_amulet.attack
            self.defense += self.equipped_amulet.defense
            self.max_health += self.equipped_amulet.health
            self.current_health += self.equipped_amulet.health

        # Remove the equipped item from the inventory
        self.inventory.remove(item)
        self.save()

    def get_equipped_items(self):
        equipped_items = []
        if self.equipped_weapon:
            equipped_items.append(self.equipped_weapon)
        if self.equipped_body_armour:
            equipped_items.append(self.equipped_body_armour)
        if self.equipped_helmet:
            equipped_items.append(self.equipped_helmet)
        if self.equipped_leg_armor:
            equipped_items.append(self.equipped_leg_armor)
        if self.equipped_ring1:
            equipped_items.append(self.equipped_ring1)
        if self.equipped_ring2:
            equipped_items.append(self.equipped_ring2)
        if self.equipped_amulet:
            equipped_items.append(self.equipped_amulet)
        return equipped_items
    
    def get_inventory_items(self):
        return self.inventory.all()

    def increase_level(self):
        # Define the XP required for each level in a dictionary
        xp_requirements = {
            1: 100,
            2: 250,
            3: 450,
            4: 700,
            5: 1000,
            # ... add more levels and XP requirements ...
        }

        class_stats = {
            "warrior": {"max_health": 10, "attack": 2, "defense": 1},
            "rogue": {"max_health": 8, "attack": 5, "defense": 0},
            "mage": {"max_health": 5, "attack": 7, "defense": 0},
            # ... add more classes and their respective stat adjustments ...
        }

        # Check if the player's current XP is enough to reach the next level
        if self.xp >= xp_requirements.get(self.level, 0):
            self.level += 1             
            class_name = self.character_class.class_type.lower()

            # Adjust stats based on the player's class
            if class_name in class_stats:
                stats = class_stats[class_name]
                self.max_health += stats["max_health"]
                self.current_health = self.max_health
                self.attack += stats["attack"]
                self.defense += stats["defense"]
            self.save()
            
            return True  # Level increased
        return False  # Level did not increase

    def attack_enemy(self, enemy_instance):
        # Calculate the damage dealt by the player
        enemy = enemy_instance.enemy
        damage_range = random.randint(-5, 5)  # Generate a random value within -5 and +5
        modified_attack = self.attack + damage_range

        # Ensure damage is non-negative
        modified_attack = max(modified_attack, 0)

        # Reduce the enemy's health based on the damage dealt
        enemy_instance.current_health -= modified_attack
        enemy_instance.current_health = max(enemy_instance.current_health, 0)  # Ensure enemy health doesn't go below 0

        # # Check if the enemy is defeated
        if enemy_instance.current_health <= 0:
            # Handle enemy defeat (e.g., grant player experience points, rewards, etc.)
            self.money += enemy.gold
            self.xp += enemy.xp
            drops = enemy_instance.drop_items()
            for item in drops:
                self.inventory.add(item)
        # Save the updated player and enemy objects to the database
        self.save()
        enemy_instance.save()
        return modified_attack

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("player_detail", kwargs={"pk": self.player_id})

class Item(models.Model):
    WEAPON = "Weapon"
    BODY_ARMOR = "Body Armor"
    HELMET = "Helmet"
    LEG_ARMOR = "Leg Armor"
    RING = "Ring"
    AMULET = "Amulet"
    MISC = "Misc"

    ITEM_TYPES = [
        (WEAPON, _("Weapon")),
        (BODY_ARMOR, _("Body Armor")),
        (HELMET, _("Helmet")),
        (LEG_ARMOR, _("Leg Armor")),
        (RING, _("Ring")),
        (AMULET, _("Amulet")),
        (MISC, _("Misc")),
    ]

    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), blank=True, null=True)
    type = models.CharField(_("type"), max_length=50, choices=ITEM_TYPES)
    attack = models.IntegerField(_("attack"), default=0)
    defense = models.IntegerField(_("defense"), default=0)
    health = models.IntegerField(_("health"), default=0)
    special_attributes = models.JSONField(_("speccial_attributes"), default=dict, blank=True, null=True)
    

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})



class CharacterClass(models.Model):
    class_type = models.CharField(_("class_type"), max_length=50, choices=CHARACTER_CLASSES)
    image = models.ImageField(_("image"), upload_to="class_images", height_field=None, width_field=None, max_length=None, blank=True, null=True)
    health = models.IntegerField(_("health"), default=0)
    attack = models.IntegerField(_("attack"), default=0)
    defense = models.IntegerField(_("defense"), default=0)

    class Meta:
        verbose_name = _("characterClass")
        verbose_name_plural = _("characterClasss")

    def __str__(self):
        return self.class_type

    def get_absolute_url(self):
        return reverse("characterClass_detail", kwargs={"pk": self.pk})

class Enemy(models.Model):
    name = models.CharField(_("name"), max_length=50)
    max_health = models.IntegerField(_("max_health"), default=0)
    current_health = models.IntegerField(_("current_health"), default=0)
    attack = models.IntegerField(_("attack"), default=0)
    defense = models.IntegerField(_("defense"), default=0)
    image = models.ImageField(_("image"), upload_to="enemy_images", height_field=None, width_field=None, max_length=None, blank=True, null=True)
    level = models.IntegerField(_("level"), default=1)
    gold = models.IntegerField(_("gold"), default=0)
    xp = models.IntegerField(_("experience"), default=10)
    drops = models.ManyToManyField(
        Item,
        verbose_name=_("drops"),
        related_name="drops",
        blank=True
    )

    class Meta:
        verbose_name = _("enemy")
        verbose_name_plural = _("enemies")

    def get_absolute_url(self):
        return reverse("enemy_detail", kwargs={"pk": self.pk})


class Location(models.Model):
    name = models.CharField(_("name"), max_length=150, blank=True, null=True)
    description = models.CharField(_("description"), max_length=1000, blank=True, null=True)
    enemy = models.ManyToManyField(
        Enemy, 
        verbose_name=_("enemies"), 
        blank=True,
    )
    victory_message = models.CharField(_("victory_message"), max_length=2000, blank=True, null=True)
    defeat_message = models.CharField(_("defeat_message"), max_length=2000, blank=True, null=True)

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("location_detail", kwargs={"pk": self.pk})

class EnemyInstance(models.Model):
    enemy = models.ForeignKey(
        Enemy,
        verbose_name=_("enemy"),
        on_delete=models.CASCADE,
        related_name="enemy_instances"
    )
    current_health = models.IntegerField(_("current_health"), default=0)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set the default value if the object is being created
            self.current_health = self.enemy.max_health
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("enemyInstances")
        verbose_name_plural = _("enemyInstancess")

    def attack_player(self, player):
        # Calculate the damage dealt by the enemy
        damage_range = random.randint(-5, 5)  # Generate a random value within -5 and +5
        e_modified_attack = self.enemy.attack + damage_range

        # Ensure damage is non-negative
        e_modified_attack = max(e_modified_attack, 0)

        # Reduce the player's health based on the damage dealt
        player.current_health -= e_modified_attack
        player.current_health = max(player.current_health, 0)  # Ensure player health doesn't go below 0

        # Check if the player is defeated
        if player.current_health <= 0:
            # Handle player defeat (e.g., reset player attributes, display game over message, etc.)
            self.handle_player_defeat(player)

        # Save the updated enemy and player objects to the database
        self.save()
        player.save()
        return e_modified_attack

    def handle_player_defeat(self, player):
        # Reset player attributes or perform any other necessary actions
        player.delete()
        # ... other attribute resets ...

        # Save the updated player object to the database
        player.save()
    
    def drop_items(self):
        return self.enemy.drops.all()

    def __str__(self):
        return self.name

    def __str__(self):
        return self.enemy.name

    def get_absolute_url(self):
        return reverse("enemyInstances_detail", kwargs={"pk": self.pk})
