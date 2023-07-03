from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import random

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
    level = models.IntegerField(_("level"), default=1)
    xp = models.IntegerField(_("experience"), default=0)

    class Meta:
        verbose_name = _("player")
        verbose_name_plural = _("players")

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
            print(self.xp)
            print(xp_requirements)
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

    def attack_enemy(self, enemy):
        # Calculate the damage dealt by the player
        damage_range = random.randint(-5, 5)  # Generate a random value within -5 and +5
        modified_attack = self.attack + damage_range

        # Ensure damage is non-negative
        modified_attack = max(modified_attack, 0)

        # Reduce the enemy's health based on the damage dealt
        enemy.current_health -= modified_attack
        enemy.current_health = max(enemy.current_health, 0)  # Ensure enemy health doesn't go below 0

        # # Check if the enemy is defeated
        if enemy.current_health <= 0:
            # Handle enemy defeat (e.g., grant player experience points, rewards, etc.)
            self.money += enemy.gold
            self.xp += enemy.xp  # Assuming you have a method to handle experience gain
            self.increase_level()
        # Save the updated player and enemy objects to the database
        self.save()
        enemy.save()
        return modified_attack

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("player_detail", kwargs={"pk": self.player_id})



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

    class Meta:
        verbose_name = _("enemy")
        verbose_name_plural = _("enemies")

    def attack_player(self, player):
        # Calculate the damage dealt by the enemy
        damage_range = random.randint(-5, 5)  # Generate a random value within -5 and +5
        e_modified_attack = self.attack + damage_range

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

    def __str__(self):
        return self.name

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

class EnemyInstances(models.Model):
    enemy = models.ForeignKey(
        Enemy,
        verbose_name=_("enemy"),
        on_delete=models.CASCADE,
        related_name="enemy"
    )
    

    class Meta:
        verbose_name = _("enemyInstances")
        verbose_name_plural = _("enemyInstancess")

    def __str__(self):
        return self.enemy

    def get_absolute_url(self):
        return reverse("enemyInstances_detail", kwargs={"pk": self.pk})
