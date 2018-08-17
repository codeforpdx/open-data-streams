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
    url(r'^db', cataloger.views.db, name='db'),
    path('admin/', admin.site.urls),
]
