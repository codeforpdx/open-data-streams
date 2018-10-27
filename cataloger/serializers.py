from rest_framework import serializers

from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('publisher', 'distribution', 'schema', 'mtype', 'title', 'description', 'keywords', 'identifier', 'accessLevel', 'bureauCode', 'programCode', 'license', 'spatial', 'temporal', 'describedByType', 'describedBy', 'accrualPeriodicity', 'conformsTo', 'dataQuality', 'isPartOf', 'issued', 'language', 'landingPage', 'primaryITInvestment', 'references', 'systemOfRecords', 'theme')
        depth = 2

class CatalogSerializer(serializers.Serializer):
    _context = serializers.URLField(label='@context', initial='https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld')
    _id = serializers.URLField(label='@id')
    _type = serializers.CharField(label='@type', initial='dcat:Catalog')
    _conformsTo = serializers.URLField(label='@conformsTo', initial='https://project-open-data.cio.gov/v1.1/schema')
    describedBy = serializers.URLField(initial='https://project-open-data.cio.gov/v1.1/schema/catalog.json')
    dataset = DatasetSerializer(required=False)
