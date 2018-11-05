# REST Framework
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from .serializers import DatasetSerializer, CatalogSerializer
from cataloger.models import Dataset, Catalog, Profile

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    """
    View to list the catalog
    """
    if request.method == 'GET':
        # there should only be 1 catalog
        catalog = Catalog.objects.all().first()
        context = {'request':request}
        serializer = CatalogSerializer(catalog, context=context)
    return Response(serializer.data)

@permission_classes((permissions.AllowAny,))
class DatasetList(APIView):
    def get(self, request, format=None):
        dataset = Dataset.objects.filter(publisher=Profile(id=request.user.id))
        context = {'request':request, 'dataset':dataset}
        serializer = DatasetSerializer(dataset, many=True, context=context)
        return Response(serializer.data)

@permission_classes((permissions.AllowAny,))
class DatasetDetail(APIView):

    def get(self, request, dataset_id=None, format=None):
        dataset = get_object_or_404(Dataset, id=dataset_id, publisher=Profile(id=request.user.id))
        context = {'request':request, 'dataset':dataset}
        serializer = DatasetSerializer(dataset, context=context)
        return Response(serializer.data)
