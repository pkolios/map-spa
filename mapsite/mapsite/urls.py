from django.conf.urls import url
from django.contrib import admin

import mapapp.views

urlpatterns = [
    url(r'^address/', mapapp.views.post_address, name='post_address'),
    url(r'^purge_fusion/', mapapp.views.purge_fusion, name='purge_fusion'),
    url(r'^purge_db/', mapapp.views.purge_db, name='purge_db'),
    url(r'^oauth2callback/', mapapp.views.oauth2callback,
        name='oauth2callback'),
    url(r'^admin/', admin.site.urls),
    url(r'^', mapapp.views.index, name='index'),
]
