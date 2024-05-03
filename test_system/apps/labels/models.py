import uuid
from django.db import models
from django.core.exceptions import ValidationError
from test_system.apps.medias.models import Medias
from test_system.apps.users.models import CustomUser

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
    user = models.ForeignKey(CustomUser, related_name="labels", on_delete=models.CASCADE)
    preset_type = models.CharField(
        max_length=255, choices=PresetTypes.choices, blank=False, null=False
    )
    custom_preset_type = models.CharField(max_length=255, null=True, blank=True)
    preset_tag = models.CharField(max_length=255 , choices=PresetTags.choices, null=False, blank=False)
    medias = models.ForeignKey(Medias, related_name= "labels", on_delete=models.CASCADE)

    def clean(self):
        if self.preset_type == PresetTypes.CUSTOM:
            if not self.custom_preset_type:
                return ValidationError("Error, please enter custom type.")
            if not self.custom_preset_type.isalnum():
                return ValidationError("Invalid input.")
        else:
            self.custom_preset_type is None
