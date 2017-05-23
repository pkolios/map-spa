from django import forms

from . import models


class AddressForm(forms.ModelForm):

    class Meta:
        model = models.Address
        fields = ('full_address', 'lat', 'lon')
