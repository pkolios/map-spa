from django.http import (
    HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse)
from django.shortcuts import render

from . import forms, models


def index(request):
    addresses = models.Address.objects.all()
    return render(request, 'index.html', {'addresses': addresses})


def post_address(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = forms.AddressForm(request.POST)
    if form.is_valid():
        form.save()
        data = [address.to_dict() for address in models.Address.objects.all()]
        return JsonResponse(data, safe=False)

    return HttpResponseBadRequest(form.errors.as_json())
