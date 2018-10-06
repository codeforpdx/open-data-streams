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
    path('new-dataset/', cataloger.views.new_dataset, name='new-dataset'),
    path('ajax/load-divisions/', cataloger.views.load_divisions, name='ajax_load_divisions'),
    path('ajax/load-offices/', cataloger.views.load_offices, name='ajax_load_offices'),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
