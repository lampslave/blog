from __future__ import unicode_literals
from django.conf.urls import include, url

from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('lbe.urls', namespace='lbe')),
]

handler404 = 'lbe.views.e404'
