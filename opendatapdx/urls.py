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
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

#
# API implementation using Django REST framework
#
from rest_framework.decorators import api_view
from rest_framework.urlpatterns import format_suffix_patterns

# Views and ViewSets define the view behavior.
from cataloger.views import api_root, DatasetList, DatasetDetail

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += format_suffix_patterns([
    path('api/', api_root),
    path('api/dataset/', DatasetList.as_view()),
    path('api/dataset/<int:dataset_id>/', DatasetDetail.as_view()),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework'))
])
