from cataloger.models import Dataset, Profile, Schema
from django.db.models import Q

COMPLETED_DATASETS = Dataset.objects.filter(complete=True)
PUBLISHED_DATASETS = Dataset.objects.filter(published=True)


def filtered_datasets(request):
    if request.user.is_superuser:
        datasets = COMPLETED_DATASETS
    elif request.user.is_authenticated:
        datasets = COMPLETED_DATASETS.filter(Q(publisher=Profile(id=request.user.id)) | Q(published=True))
    else:
        datasets = PUBLISHED_DATASETS
    return datasets


# UNTESTED
# def filtered_schema(request):
#     return filtered_datasets(request).select_related('schema')
