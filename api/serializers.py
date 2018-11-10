from rest_framework import serializers

from cataloger.models import Dataset, Catalog, Profile, Keyword, BureauCode, Distribution, License, AccessLevel, Division, Language

class PublisherSerializer(serializers.ModelSerializer):
    publisher = serializers.CharField()

    class Meta:
        model = Profile
        fields = ('publisher',)

    def to_representation(self, value):
        profile = Profile.objects.get(username=value)
        publisher = {"@type":"org:Organization", "name": str(profile.office), "subOrganizationOf":{"@type":"org:Organization", "name": str(profile.division), "subOrganizationOf": {"@type":"org:Organization", "name": str(profile.bureau), "subOrganizationOf": {"@type":"org:Organization", "name":"City"}}}}
        return publisher


class KeywordSerializer(serializers.ModelSerializer):
    keyword = serializers.CharField()

    class Meta:
        model = Keyword
        fields = ('keyword',)

    def to_representation(self, value):
        return str(value)


class ProgramCodeSerializer(serializers.ModelSerializer):
    programCode = serializers.CharField()

    class Meta:
        model = Division
        fields = ('programCode',)

    def to_representation(self, value):
        return str(value.division)


class LicenseSerializer(serializers.ModelSerializer):
    license = serializers.URLField(source='url')

    class Meta:
        model = License
        fields = ('license',)

    def to_representation(self, value):
        return str(value.url)


class AccessLevelSerializer(serializers.ModelSerializer):
    accessLevel = serializers.CharField()

    class Meta:
        model = AccessLevel
        fields = ('accessLevel',)

    def to_representation(self, value):
        return str(value)


class ContactPointSerializer(serializers.Serializer):
    contactPoint = serializers.CharField()

    def to_representation(self, instance):
        try:
            contactPoint = {'@type': 'vcard:Contact',
                            'fn': instance.username,
                            'hasEmail': 'mailto:'+instance.email}
        except:
            contactPoint = {}
        return contactPoint

class BureauCodeSerializer(serializers.Serializer):
    bureauCode = serializers.CharField()

    class Meta:
        model = BureauCode
        fields = ("bureauCode",)

    def to_representation(self, value):
        return str(value.code)

class DistributionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Distribution
        fields = ('@type', 'title', 'description', 'downloadURL', 'format', 'accessURL', 'describedBy', 'describedByType', 'conformsTo', 'mediaType',)

class LanguageSerializer(serializers.Serializer):
    Language = serializers.CharField()

    class Meta:
        model = Language
        fields = ("language",)

    def to_representation(self, value):
        return str(value.language)

# rename the "mtype" field to "@type" in the serializer's _declared_fields
DistributionSerializer._declared_fields['@type'] = serializers.CharField(source='mtype')
# rename the "dformat" field to "format" in the serializer's _declared_fields
DistributionSerializer._declared_fields['format'] = serializers.CharField(source='dformat')


class DatasetSerializer(serializers.ModelSerializer):
    keyword = KeywordSerializer(many=True)
    publisher = PublisherSerializer()
    contactPoint = ContactPointSerializer(source='publisher')
    bureauCode = BureauCodeSerializer(many=True)
    distribution = DistributionSerializer(many=True, source='distribution_set')
    license = LicenseSerializer()
    accessLevel = AccessLevelSerializer()
    programCode = ProgramCodeSerializer(many=True)
    language = LanguageSerializer(many=True)

    class Meta:
        model = Dataset
        fields = ('@type', 'title', 'description', 'keyword', 'modified', 'publisher', 'contactPoint', 'identifier', 'accessLevel', 'bureauCode', 'programCode', 'license', 'rights', 'spatial', 'temporal', 'distribution', 'accrualPeriodicity', 'conformsTo', 'dataQuality', 'dataQuality', 'describedBy', 'describedByType', 'isPartOf', 'issued', 'language', 'landingPage', 'primaryITInvestment', 'references', 'systemOfRecords', 'theme')
        depth = 2

# rename the "mtype" field to "@type" in the serializer's _declared_fields
DatasetSerializer._declared_fields['@type'] = serializers.CharField(source='mtype')


class CatalogSerializer(serializers.ModelSerializer):
    dataset = DatasetSerializer(many=True, source='dataset_set')

    class Meta:
        model = Catalog
        fields = ('@context', '@id', '@type', '@conformsTo', 'describedBy', 'dataset')
        depth = 2

# rename the "_context", "_id", "_type", and "_conformsTo" fields to have the '@' prefix rather than a '_' in the serializer's _declared_fields
CatalogSerializer._declared_fields['@context'] = serializers.URLField(source='_context')
CatalogSerializer._declared_fields['@id'] = serializers.URLField(source='_id')
CatalogSerializer._declared_fields['@type'] = serializers.URLField(source='_type')
CatalogSerializer._declared_fields['@conformsTo'] = serializers.URLField(source='_conformsTo')
