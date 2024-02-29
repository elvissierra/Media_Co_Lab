import uuid
from django.db import models
from django.core.exceptions import ValidationError


class PresetTypes(models.TextChoices):
    ART = "art"
    MUSIC = "music"
    SPORT = "sport"
    GAME = "game"
    LITERATURE = "literature"
    FILM = "film"
    TECHNOLOGY = "technology"
    CUSTOM = "custom"

class PresetTags(models.TextChoices):
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"

class Label(models.Model):
    title = models.CharField(max_length=255)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.CharField(max_length=255, blank=False, null=False)
    preset_type = models.CharField(
        max_length=255, choices=PresetTypes.choices, blank=False, null=False
    )
    custom_preset_type = models.CharField(max_length=255, null=True, blank=True)
    preset_tag = models.CharField(max_length=255 , choices=PresetTags.choices, null=False, blank=False)
    

    def clean(self):
        if self.preset_type == PresetTypes.CUSTOM:
            if not self.custom_preset_type:
                return ValidationError("Error, please enter custom type.")
            if not self.custom_preset_type.isalnum():
                return ValidationError("Invalid input.")
        else:
            self.custom_preset_type == None


    def save(self, *args, **kwargs):
        self.full_clean()
        self.layer_width = self.bottom_depth - self.top_depth
        super().save(*args, **kwargs)
