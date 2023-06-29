from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class Player(models.Model):
    player_id = models.CharField(_("player ID"), max_length=50, primary_key=True)
    username = models.CharField(_("username"), max_length=50)
    
    class Meta:
        verbose_name = _("player")
        verbose_name_plural = _("players")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("player_detail", kwargs={"pk": self.player_id})