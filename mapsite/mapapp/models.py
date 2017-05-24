from django.db import models
from django.forms.models import model_to_dict


class Address(models.Model):
    """Represents the address data stored locally."""

    full_address = models.CharField(max_length=250)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.full_address

    def to_dict(self):
        """Cast model to dict."""
        return model_to_dict(self)
