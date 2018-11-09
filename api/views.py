# REST Framework
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from .serializers import DatasetSerializer, CatalogSerializer
from cataloger.models import Profile, Schema
from .dataset_filter import filtered_datasets
import json

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    """
    View to list the catalog
    """
    if request.method == 'GET':
        # there should only be 1 catalog
        # catalog = Catalog.objects.all().first()
        catalog = {"_context": "https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld",
                   "_id": "https://opendatapdx.herokuapp.com/api/",
                   "_type": "dcat:Catalog",
                   "_conformsTo": "https://project-open-data.cio.gov/v1.1/schema",
                   "describedBy": "https://project-open-data.cio.gov/v1.1/schema/catalog.json",
                   "dataset_set": filtered_datasets(request)}
        context = {'request': request}
        serializer = CatalogSerializer(catalog, context=context)
    return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class DatasetList(APIView):
    def get(self, request, format=None):
        dataset = filtered_datasets(request)
        context = {'request': request, 'dataset': dataset}
        serializer = DatasetSerializer(dataset, many=True, context=context)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class DatasetDetail(APIView):

    def get(self, request, dataset_id=None, format=None):
        dataset = get_object_or_404(filtered_datasets(request), id=dataset_id, publisher=Profile(id=request.user.id))
        context = {'request': request, 'dataset': dataset}
        serializer = DatasetSerializer(dataset, context=context)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class SchemaDetail(APIView):

    def get(self, request, schema_id=None, format=None):
        schema = get_object_or_404(Schema, id=schema_id)
        return Response(json.loads(schema.data))
