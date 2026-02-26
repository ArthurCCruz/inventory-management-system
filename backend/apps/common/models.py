from django.conf import settings
from django.db import models

class OwnedModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Unit(models.TextChoices):
    KG = "kg"
    G = "g"
    UNIT = "unit"
    L = "l"
    ML = "ml"