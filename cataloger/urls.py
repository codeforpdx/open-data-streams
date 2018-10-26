from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import cataloger.views

# Examples:
# url(r'^$', 'opendatapdx.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

app_name = 'cataloger'
urlpatterns = [
    path('', cataloger.views.index, name='index'),
    path('register/', cataloger.views.register, name='register'),
    path('dashboard/', cataloger.views.dashboard, name='dashboard'),
    path('dataset/<int:dataset_id>/', cataloger.views.dataset, name='dataset'),
    path('distribution/<int:distribution_id>/', cataloger.views.distribution, name='distribution'),
    path('schema/<int:schema_id>/', cataloger.views.schema, name='schema'),
    path('utilities/', cataloger.views.utilities),
    path('new_dataset/', cataloger.views.new_dataset, name='new_dataset'),
    path('ajax/load-divisions/', cataloger.views.load_divisions, name='ajax_load_divisions'),
    path('ajax/load-offices/', cataloger.views.load_offices, name='ajax_load_offices'),
]
