# REST Framework
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound

from rest_framework import serializers, pagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from .pagination import LimitOffsetPaginationDataOnly

from .serializers import DatasetSerializer, CatalogSerializer
from cataloger.models import Profile, Schema, Dataset
from .dataset_filter import filtered_datasets
import json


@permission_classes((permissions.AllowAny,))
class CatalogList(ListAPIView):
    serializer_class = CatalogSerializer
    permission_classes = (permissions.AllowAny)
    pagination_class = LimitOffsetPaginationDataOnly
    
    def list(self, request):
        result = self.paginator.paginate_queryset(self.get_queryset(),request)
        catalog = {"_context": "https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld",
                   "_id": "https://opendatapdx.herokuapp.com/api/",
                   "_type": "dcat:Catalog",
                   "_conformsTo": "https://project-open-data.cio.gov/v1.1/schema",
                   "describedBy": "https://project-open-data.cio.gov/v1.1/schema/catalog.json",
                   "dataset_set": result}
        serializer = CatalogSerializer(catalog)
        return Response(serializer.data)

    def get_queryset(self):
        return filtered_datasets(self.request)


@permission_classes((permissions.AllowAny,))
class DatasetList(ListAPIView):
    serializer_class = DatasetSerializer
    permission_classes = (permissions.AllowAny)
    pagination_class = LimitOffsetPaginationDataOnly

    def get_queryset(self):
        return filtered_datasets(self.request)


@permission_classes((permissions.AllowAny,))
class DatasetDetail(RetrieveAPIView):
    serializer_class = DatasetSerializer
    permission_classes = (permissions.AllowAny)
    
    def retrieve(self, request, dataset_id=None, format=None):
        try:
            queryset = filtered_datasets(request).get(id=dataset_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Not found")
        serializer = DatasetSerializer(queryset)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class SchemaDetail(RetrieveAPIView):

    def get(self, request, schema_id=None, format=None):
        schema = get_object_or_404(Schema, id=schema_id)
        return Response(json.loads(schema.data))
