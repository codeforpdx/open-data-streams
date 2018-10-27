from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser

from .managers import ProfileManager

class AccessLevel(models.Model):
    """
    AccessLevel represents the POD 1.1 accessLevel field
    
    https://project-open-data.cio.gov/v1.1/schema/#accessLevel
    
    Accepted Values:
        This field accepts the following values:
        
        - **Public**: This information might not need to be disclosed, but if it is, it shouldn’t cause any damage.
        - **Sensitive**: This information requires a greater level of protection to prevent loss of inappropriate disclosure.
        - **Private**: This information is for agency use only, and its disclosure would damage the public trust placed in the agency.
        - **Confidential**: This is the highest level of sensitivity, and disclosure could cause extreme damage to the agency’s ability to perform its primary business function. Datasets containing information whose disclosure could lead directly to massive financial loss, danger to public safety, or lead to loss of life is classified as confidential.
        
    Stores a single AccessLevel, related to :model:`cataloger.Dataset`
    
    Note:
        The Accepted Values of the original `accessLevel`_ definition
        specified:
        
            Must be one of the following: “public”, “restricted public”, “non-public”
        
    .. _accessLevel: https://project-open-data.cio.gov/v1.1/schema/#accessLevel
    """
    accessLevel = models.CharField(max_length=12, default=3)
    description = models.TextField()

    def __str__(self):
        return self.accessLevel

class License(models.Model):
    """
    License represents the POD 1.1 license field
    
    https://project-open-data.cio.gov/v1.1/schema/#license
    
    Accepted Values:
        The Accepted Values of the `license`_ field are:
    
        - *Creative Commons CCZero* (**CC0**)
    
        - *Open Data Commons Public Domain Dedication and Licence* (**PDDL**)
    
        - *Creative Commons Attribution 4.0* (**CC-BY-4.0**)
    
        - *Open Data Commons Attribution License* (**ODC-BY**)
    
        - *Creative Commons Attribution Share-Alike 4.0* (**CC-BY-SA-4.0**)
    
        - *Open Data Commons Open Database License* (**ODbL**)
        
        
    .. _license: https://project-open-data.cio.gov/v1.1/schema/#license
    """
    license = models.CharField(max_length=12, default=3)
    description = models.TextField()

    def __str__(self):
        return self.description

class Keyword(models.Model):
    """
    Keyword represents the POD 1.1 keyword field
    
    https://project-open-data.cio.gov/v1.1/schema/#keyword

    Accepted Values:
        Any Unicode string value
        
    Note:
        The Values of the `keyword`_ field will be strings
        
    .. _keyword: https://project-open-data.cio.gov/v1.1/schema/#keyword
    """
    keyword = models.TextField()

    def __str__(self):
        return self.keyword

class Language(models.Model):
    """
    License represents the POD 1.1 language field
    
    https://project-open-data.cio.gov/v1.1/schema/#language
    
    Accepted Values:
        This should adhere to the RFC 5646 standard.
        
        Example: "**en-US**", "**es-MX**", "**wo**", "**nv**", "**en-US**", etc.
    
    Note:
        Language codes are pre-loaded using *initial_data.json* fixture. New
        language codes should either be manually created via /admin interface,
        or the fixtures file should be expanded with the new entries.
    
    .. _language: https://project-open-data.cio.gov/v1.1/schema/#language
    """
    language = models.CharField(max_length=10)
    description = models.TextField()
    
    def __str__(self):
        return self.description

# City bureau codes, divisions, and offices
class BureauCode(models.Model):
    """
    BureauCode represents the POD 1.1 bureauCode field
    
    https://project-open-data.cio.gov/v1.1/schema/#bureauCode
    
    Accepted Values:
        2-letter City of Portland `bureauCode`_ (e.g., "AT", "AU", "BO", etc.)
        
    .. _bureauCode: https://project-open-data.cio.gov/v1.1/schema/#bureauCode
    """
    code = models.TextField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.description

class Division(models.Model):
    """
    Division relates the POD 1.1 **bureauCode** field to the **programCode** field
    
    Although the programCode field has its value set to :model:`cataloger.Office`, the :model:`cataloger.Division` instances are used to narrow down the list of :model:`cataloger.Office` objects presented to a user on the `/registration`_ page
    
    Accepted Values:
        4-digit City of Portland division code (e.g., "ATAT", "AUCA", "BOBO", etc.)
        
    Note:
        This class is not specifically required, but its existence helps to filter/narrow down the list of options when configuring a Profile's related Office via the `/registration`_ page
        
    .. _/registration: https://localhost:8000/registration
    """
    bureau = models.ForeignKey(BureauCode, on_delete=models.CASCADE)
    division = models.TextField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.description

class Office(models.Model):
    """
    Office represents the POD 1.1 **programCode** field
    
    Accepted Values:
        10-digit City of Portland division code (e.g., "ATAT000001", "AUCA000001", "BOBO000001", etc.)
        
    Note:
        This class is being used as the POD 1.1 `programCode`_, rather than the :model:`cataloger.Division` class, but the latter is still required for ease of use when displaying the registration form to users
        
    .. _programCode: https://project-open-data.cio.gov/v1.1/schema/#programCode

    """
    bureau = models.ForeignKey(BureauCode, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    office = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description

# Notice that first name, last name, and email are not columns here. That is
# because Django includes them as columns in the AbstractUser object, which Profile extends.
class Profile(AbstractUser):
    """
    Profile represents a user account that has been registered on the system.
    
    Although this field doesn't exactly match the `publisher`_ or `contactPoint`_ fields defined by the `POD 1.1 schema`_, it is used to relate a Profile to a :model:`cataloger.Dataset` instance, and is also used to fill the aforementioned fields based on Profile field values.
        
    Note:
        This class is being used as a way to relate Profiles to Dataset instances via the `publisher`_ field. Although the `POD 1.1 schema` defines `publisher`_ as a nested list of organizations, those orgs are resolved based on the user's :model:`cataloger.Office`, and :model:`cataloger.Division`; :model:`cataloger.BureauCode` relations. Similarly, the `contactPoint`_ field will be filled from Profile member fields.
        
    .. _publisher: https://project-open-data.cio.gov/v1.1/schema/#publisher
    .. _contactPoint: https://project-open-data.cio.gov/v1.1/schema/#contactPoint
    .. _POD 1.1 schema: https://project-open-data.cio.gov/v1.1/schema/

    """
    bureau = models.ForeignKey(BureauCode, on_delete=models.SET_NULL, null=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True)
    # Set the custom UserManager for this class (for custom create_user() function call handling)
    objects = ProfileManager()

class Schema(models.Model):
    """
    Schema represents a user-generated Schema
    
    These objects are referred to via the URL specified in the `describedBy`_ field of a :model:`cataloger.Dataset` instance.
    
    Schema objects are (in most instances) created by the *schema_generator.py* module, and have their **data** field (a JSONField object) set to the JSON text blob that was generated.
    
    Accepted Values:
        JSON-formatted string
        
    Note:
        The model's **data** field should include a JSON key ($schema) that specifies the format of the JSON blob. In most cases, that format will be based on `JSON Schema draft-07`_

    .. _JSON Schema draft-07: http://json-schema.org/draft-07
    .. _describedBy: https://project-open-data.cio.gov/v1.1/schema/#describedBy
    """
    data = JSONField()

class Distribution(models.Model):
    """
    Distribution represent a single distribution within a POD 1.1 dataset
    
    These objects are related to a unique :model:`cataloger.Dataset` instance.
    
    Note:
        The POD 1.1 definition of the `distribution`_ field specifies that it should be an array of `distribution`_ objects, but this implementation uses a OneToOneField to relate those objects. This implies that the current implementation is not fully POD 1.1 compliant.

    .. _distribution: https://project-open-data.cio.gov/v1.1/schema/#distribution
    """
    mtype = models.TextField(default='dcat:Distribution',blank=True)
    accessURL = models.TextField(blank=True)
    conformsTo = models.TextField(blank=True)
    describedBy = models.TextField(blank=True)
    describedByType = models.TextField(blank=True)
    description = models.TextField(blank=True)
    downloadURL = models.TextField(blank=True)
    # format field (renamed since format is a reserved Python keyword)
    dformat = models.TextField(blank=True)
    mediaType = models.TextField(blank=True)
    title = models.TextField(blank=True)

class Dataset(models.Model):
    """
    Dataset represent a single dataset stored within a POD 1.1 catalog
    
    These objects are related to a single :model:`cataloger.Profile` via the `publisher`_ relation.
    
    Note:
        The POD 1.1 definition of the `dataset`_ field specifies that it should be an array of `dataset`_ objects contained within a `catalog`_, but this implementation omits the enclosing `catalog`_, and simply outputs all :model:`cataloger.Dataset` instances within a JSON-formatted POD 1.1 `catalog`_ on the fly.

    .. _publisher: https://project-open-data.cio.gov/v1.1/schema/#publisher
    .. _dataset: https://project-open-data.cio.gov/v1.1/schema/#dataset
    .. _catalog: https://project-open-data.cio.gov/v1.1/schema/#catalog
    """
    # ---------- FOREIGN KEYS ----------
    # Relates a dataset to the user that published it.
    publisher = models.ForeignKey(Profile, on_delete=models.PROTECT)
    # Relates a dataset to its distribution.
    distribution = models.OneToOneField(Distribution, on_delete=models.CASCADE)
    # Relates a dataset to its schema.
    schema = models.OneToOneField(Schema, on_delete=models.CASCADE)

    # ---------- DATASET FIELDS ----------
    # @type field (renamed since type is a reserved Python keyword)
    mtype = models.TextField(default='dcat:Dataset',)
    title = models.TextField()
    description = models.TextField()
    # Could be a string that is a comma separated list.
    keywords = models.ManyToManyField(Keyword)
    modified = models.DateTimeField(auto_now_add=True)
    # Will store the URL to this dataset.
    identifier = models.URLField()
    accessLevel = models.ForeignKey(AccessLevel, on_delete=models.PROTECT, default=2)
    bureauCode = models.ManyToManyField(BureauCode)
    programCode = models.ManyToManyField(Division)
    license = models.ForeignKey(License, on_delete=models.PROTECT, default=3)

    # If applicable.
    spatial = models.TextField(blank=True)
    temporal = models.TextField(blank=True)

    # contactPoint -- doesn't exist as a field of Dataset. Instead, use the publisher's info.
    # (although we might decide to include this as a field or do this differently)

    describedByType = models.TextField(blank=True)
    # Will store an API url for this dataset's schema.
    describedBy = models.TextField(blank=True)

    # All dataset fields below this comment are (tentatively) to remain empty for this project.
    accrualPeriodicity = models.TextField(blank=True)
    conformsTo = models.TextField(blank=True)
    dataQuality = models.BooleanField(blank=True, default=False)
    isPartOf = models.TextField(blank=True)
    issued = models.TextField(blank=True)
    language = models.ManyToManyField(Language, blank=True, default=57)
    landingPage = models.TextField(blank=True)
    primaryITInvestment = models.TextField(blank=True)
    references = models.TextField(blank=True)
    systemOfRecords = models.TextField(blank=True)
    theme = models.TextField(blank=True)

class Catalog(models.Model):
    _context = models.URLField(default='https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld')
    _id = models.URLField(default='https://opendatapdx.herokuapp.com/api/')
    _type = models.CharField(default='dcat:Catalog', max_length=12)
    _conformsTo = models.URLField(default='https://project-open-data.cio.gov/v1.1/schema')
    describedBy = models.URLField(default='https://project-open-data.cio.gov/v1.1/schema/catalog.json')
    dataset = models.ForeignKey(Dataset, on_delete=models.PROTECT)
