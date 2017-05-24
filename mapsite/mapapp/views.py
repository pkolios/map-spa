from django.http import (
    HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse)
from django.conf import settings
from django.core.management import call_command
from django.shortcuts import redirect, render
from oauth2client import client

from . import forms, fusion, models


def index(request):
    """Render index that contains list of all existing addresses."""
    if settings.ENABLE_GOOGLE_FUSION:
        try:
            fusion.FusionAPI(request, settings)
        except fusion.LoginRequired as exc:
            return redirect('oauth2callback')

    addresses = models.Address.objects.all()
    return render(request, 'index.html', {'addresses': addresses})


def post_address(request):
    """Store a new address, and return a new list with all addresses."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = forms.AddressForm(request.POST)
    if form.is_valid():
        address = form.save(commit=False)
        if settings.ENABLE_GOOGLE_FUSION:
            fusion_api = fusion.FusionAPI(request, settings)
            fusion_api.add_entry(address.to_dict())
        address.save()
        data = [address.to_dict() for address in models.Address.objects.all()]
        return JsonResponse(data, safe=False)

    return HttpResponseBadRequest(form.errors.as_json())


def purge_fusion(request):
    if settings.ENABLE_GOOGLE_FUSION:
        fusion_api = fusion.FusionAPI(request, settings)
        fusion_api.purge()
    return redirect('index')


def purge_db(request):
    call_command('flush', interactive=False)
    return redirect('index')


def oauth2callback(request):
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope=settings.GOOGLE_FUSION_SCOPE,
        redirect_uri=settings.GOOGLE_FUSION_REDIRECT_URL)
    flow.params['include_granted_scopes'] = 'true'
    if 'code' not in request.GET:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.GET.get('code')
        credentials = flow.step2_exchange(auth_code)
        request.session['credentials'] = credentials.to_json()
        return redirect('index')
