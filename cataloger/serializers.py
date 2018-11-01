from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Dataset, Catalog, Profile, Keyword

class PublisherField(serializers.ModelSerializer):
    profile = serializers.CharField()
    
    class Meta:
        model = Profile
        fields = ('profile',)
    
    def to_representation(self, value):
        profile = Profile.objects.get(username=value)
        publisher = {"@type":"org:Organization", "name": str(profile.office), "subOrganizationOf":{"@type":"org:Organization", "name": str(profile.division), "subOrganizationOf": {"@type":"org:Organization", "name": str(profile.bureau), "subOrganizationOf": {"@type":"org:Organization", "name":"City"}}}}
        return publisher


class KeywordField(serializers.ModelSerializer):
    keyword = serializers.CharField()
    
    class Meta:
        model = Keyword
        fields = ('keyword',)
    
    def to_representation(self, value):
        return str(value)


class ContactPointSerializer(serializers.Serializer):
    contactPoint = serializers.CharField()

    def to_representation(self, instance):
        user = None
        dataset = self.context.get("dataset")
        if dataset and hasattr(dataset, "publisher"):
            user = dataset.publisher
        if user:
            contactPoint = {'@type': 'vcard:Contact',
                            'fn': user.username,
                            'hasEmail': 'mailto:'+user.email}
        else:
            contactPoint = {}
        return contactPoint


class DatasetSerializer(serializers.ModelSerializer):
    keyword = KeywordField(many=True)
    publisher = PublisherField()
    contactPoint = ContactPointSerializer()
    
    class Meta:
        model = Dataset
        fields = ('@type', 'title', 'description', 'keyword', 'modified', 'publisher', 'contactPoint', 'identifier', 'accessLevel', 'bureauCode', 'programCode', 'license', 'rights', 'spatial', 'temporal', 'distribution', 'accrualPeriodicity', 'conformsTo', 'dataQuality', 'dataQuality', 'describedBy', 'describedByType', 'isPartOf', 'issued', 'language', 'landingPage', 'primaryITInvestment', 'references', 'systemOfRecords', 'theme')
        depth = 2

# rename the "mtype" field to "@type" in the serializer's _declared_fields
DatasetSerializer._declared_fields['@type'] = serializers.CharField(source='mtype')


class CatalogSerializer(serializers.ModelSerializer):
    dataset = DatasetSerializer(many=True)
    
    class Meta:
        model = Catalog
        fields = ('@context', '@id', '@type', '@conformsTo', 'describedBy', 'dataset')
        depth = 2

# rename the "_context", "_id", "_type", and "_conformsTo" fields to have the '@' prefix rather than a '_' in the serializer's _declared_fields
CatalogSerializer._declared_fields['@context'] = serializers.URLField(source='_context')
CatalogSerializer._declared_fields['@id'] = serializers.URLField(source='_id')
CatalogSerializer._declared_fields['@type'] = serializers.URLField(source='_type')
CatalogSerializer._declared_fields['@conformsTo'] = serializers.URLField(source='_conformsTo')
