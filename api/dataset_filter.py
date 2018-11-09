from cataloger.models import Dataset, Profile, Schema

COMPLETED_DATASETS = Dataset.objects.filter(complete=True)
PUBLISHED_DATASETS = Dataset.objects.filter(published=True)


def filtered_datasets(request):
    if request.user.is_staff:
        datasets = COMPLETED_DATASETS
    elif request.user.is_authenticated:
        datasets = COMPLETED_DATASETS.filter(publisher=Profile(id=request.user.id))
        datasets.union(PUBLISHED_DATASETS)
    else:
        datasets = PUBLISHED_DATASETS
    return datasets