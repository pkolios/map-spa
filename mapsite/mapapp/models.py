from django.db import models
from django.forms.models import model_to_dict


class Address(models.Model):

    full_address = models.CharField(max_length=250)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.full_address

    def to_dict(self):
        return model_to_dict(self)
