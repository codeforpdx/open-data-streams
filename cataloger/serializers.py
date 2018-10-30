from rest_framework import serializers

from .models import Dataset, Catalog

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('@type', 'title', 'description', 'keyword', 'modified', 'publisher', 'contactPoint', 'identifier', 'accessLevel', 'bureauCode', 'programCode', 'license', 'rights', 'spatial', 'temporal', 'distribution', 'accrualPeriodicity', 'conformsTo', 'dataQuality', 'dataQuality', 'describedBy', 'describedByType', 'isPartOf', 'issued', 'language', 'landingPage', 'primaryITInvestment', 'references', 'systemOfRecords', 'theme')
        depth = 2

# rename the "mtype" field to "@type" in the serializer's _declared_fields
DatasetSerializer._declared_fields["@type"] = serializers.CharField(source="mtype")


class CatalogSerializer(serializers.ModelSerializer):
    dataset = DatasetSerializer(many=True)
    
    class Meta:
        model = Catalog
        fields = ('@context', '@id', '@type', '@conformsTo', 'describedBy', 'dataset')
        depth = 2

# rename the "_context", "_id", "_type", and "_conformsTo" fields to have the '@' prefix rather than a '_' in the serializer's _declared_fields
CatalogSerializer._declared_fields["@context"] = serializers.URLField(source="_context")
CatalogSerializer._declared_fields["@id"] = serializers.URLField(source="_id")
CatalogSerializer._declared_fields["@type"] = serializers.URLField(source="_type")
CatalogSerializer._declared_fields["@conformsTo"] = serializers.URLField(source="_conformsTo")

