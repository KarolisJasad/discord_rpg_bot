from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

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
    attack = models.IntegerField(_("attack"), default='0')
    defense = models.IntegerField(_("defense"), default='0')
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
    
    class Meta:
        verbose_name = _("player")
        verbose_name_plural = _("players")

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

    class Meta:
        verbose_name = _("enemy")
        verbose_name_plural = _("enemies")

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

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("location_detail", kwargs={"pk": self.pk})

