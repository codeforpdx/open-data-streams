#
# API implementation using Django REST framework
#
from django.conf.urls import include
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.urlpatterns import format_suffix_patterns

# Views and ViewSets define the view behavior.
from .views import api_root, DatasetList, DatasetDetail

# Manual URL configuration for REST API is currently being used.
# Additionally, we include login URLs for the browsable API.
app_name = 'api'
urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('dataset/', DatasetList.as_view()),
    path('dataset/<int:dataset_id>/', DatasetDetail.as_view()),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
])
