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
    username = models.CharField(_("username"), max_length=50)
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
    

    class Meta:
        verbose_name = _("characterClass")
        verbose_name_plural = _("characterClasss")

    def __str__(self):
        return self.class_type

    def get_absolute_url(self):
        return reverse("characterClass_detail", kwargs={"pk": self.pk})
