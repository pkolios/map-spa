from django.conf.urls import url
from django.contrib import admin

import mapapp.views

urlpatterns = [
    url(r'^address/', mapapp.views.post_address, name='post_address'),
    url(r'^admin/', admin.site.urls),
    url(r'^', mapapp.views.index, name='index'),
]
