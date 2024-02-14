import uuid
from django.db import models
from django.core.exceptions import ValidationError


class PresetTypes(models.TextChoices):
    SANDSTONE = "sandstone"
    CEMENTED_SAND = "cemented_sand"
    SILTSTONE = "siltstone"
    SHALE_SAND = "shale_sand"
    SANDY_SHALE = "sandy_shale"
    SHALE = "shale"
    ORGANIC_RICH_MUDSTONE = "organic_rich_mudstone"
    CEMENTED_SHALE = "cemented_shale"
    MARL = "marl"
    LIMESTONE = "limestone"
    DOLOMITE = "dolomite"
    HALITE = "halite"
    ANHYDRITE = "anhydrite"
    IGNEOUS = "igneous"
    TUFF = "tuff"
    COAL_LIGNITE = "coal_lignite"
    CONGLOMERATE_BRECCIA = "conglomerate_breccia"
    BAD_HOLE = "bad_hole"
    CUSTOM = "custom"


class Label(models.Model):
    title = models.CharField(max_length=255)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.CharField(max_length=255, blank=False, null=False)
    preset_type = models.CharField(
        max_length=255, choices=PresetTypes.choices, blank=False, null=False
    )
    custom_preset_type = models.CharField(max_length=255, null=True, blank=True)
    top_depth = models.FloatField()
    bottom_depth = models.FloatField()
    layer_width = models.FloatField(null=True, blank=True)
    well_name = models.CharField(max_length=255)

    def clean(self):
        if self.preset_type == PresetTypes.CUSTOM:
            if not self.custom_preset_type:
                return ValidationError("Error occured at set preset type.")
            if not self.custom_preset_type.isalnum():
                return ValidationError("Invalid input.")
        else:
            self.custom_preset_type == None

        if self.top_depth >= self.bottom_depth:
            raise ValidationError("Top value must be less than bottom value.")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.layer_width = self.bottom_depth - self.top_depth
        super().save(*args, **kwargs)
