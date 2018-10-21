from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser

from .managers import ProfileManager

class AccessLevel(models.Model):
    """
    AccessLevel represents the POD 1.1 accessLevel field
    
    https://project-open-data.cio.gov/v1.1/schema/#accessLevel
    
    This field accepts the following values:
     
    - **Public**: This information might not need to be disclosed, but if it is, it shouldn’t cause any damage.
    - **Sensitive**: This information requires a greater level of protection to prevent loss of inappropriate disclosure.
    - **Private**: This information is for agency use only, and its disclosure would damage the public trust placed in the agency.
    - **Confidential**: This is the highest level of sensitivity, and disclosure could cause extreme damage to the agency’s ability to perform its primary business function. Datasets containing information whose disclosure could lead directly to massive financial loss, danger to public safety, or lead to loss of life is classified as confidential.
    
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
    
    Note:
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
    
    Note:
        The Values of the `keyword`_ field will be strings
        
    .. _keyword: https://project-open-data.cio.gov/v1.1/schema/#keyword
    """
    keyword = models.TextField()

    def __str__(self):
        return self.keyword

class Language(models.Model):
    language = models.CharField(max_length=10)
    description = models.TextField()
    
    def __str__(self):
        return self.description

# City bureau codes, divisions, and offices
class BureauCode(models.Model):
    code = models.TextField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.description

class Division(models.Model):
    bureau = models.ForeignKey(BureauCode, on_delete=models.CASCADE)
    division = models.TextField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.description

class Office(models.Model):
    bureau = models.ForeignKey(BureauCode, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    office = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description

# Notice that first name, last name, and email are not columns here. That is
# because Django includes them as columns in the AbstractUser object, which Profile extends.
class Profile(AbstractUser):
    bureau = models.ForeignKey(BureauCode, on_delete=models.SET_NULL, null=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True)
    # Set the custom UserManager for this class (for custom create_user() function call handling)
    objects = ProfileManager()

class Schema(models.Model):
    data = JSONField()

class Distribution(models.Model):
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
