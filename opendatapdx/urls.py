from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

# Examples:
# url(r'^$', 'opendatapdx.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    path('', include('cataloger.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
