from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import cataloger.views

# Examples:
# url(r'^$', 'opendatapdx.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', cataloger.views.index, name='index'),
    url(r'^register$', cataloger.views.register, name='register'),
    path('admin/', admin.site.urls),
    path('dashboard/', cataloger.views.dashboard),
    path('utilities/', cataloger.views.utilities),
    path('ajax/load-divisions/', cataloger.views.load_divisions, name='ajax_load_divisions'),  # <-- this one here
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
