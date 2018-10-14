from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser
from django.conf.global_settings import LANGUAGES

from .managers import ProfileManager

class AccessLevel(models.Model):
    accessLevel = models.CharField(max_length=12, default=3)

    def __str__(self):
        return self.accessLevel

class License(models.Model):
    license = models.CharField(max_length=12, default=3)
    description = models.TextField()
    
    def __str__(self):
        return self.description

class Keyword(models.Model):
    keyword = models.TextField()

    def __str__(self):
        return self.keyword

class Language(models.Model):
    language = models.CharField(max_length=7, choices=LANGUAGES, default='en')

    def __str__(self):
        return self.language

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
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE)
    # Relates a dataset to its schema.
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

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
    license = models.ForeignKey(License, on_delete=models.PROTECT, default=2)

    # If applicable.
    spatial = models.TextField()
    temporal = models.TextField()

    # contactPoint -- doesn't exist as a field of Dataset. Instead, use the publisher's info.
    # (although we might decide to include this as a field or do this differently)

    describedByType = models.TextField()
    # Will store an API url for this dataset's schema.
    describedBy = models.TextField()

    # All dataset fields below this comment are (tentatively) to remain empty for this project.
    accrualPeriodicity = models.TextField(blank=True)
    conformsTo = models.TextField(blank=True)
    dataQuality = models.BooleanField(blank=True, default=False)
    isPartOf = models.TextField(blank=True)
    issued = models.TextField(blank=True)
    language = models.ManyToManyField(Language, blank=True)
    landingPage = models.TextField(blank=True)
    primaryITInvestment = models.TextField(blank=True)
    references = models.TextField(blank=True)
    systemOfRecords = models.TextField(blank=True)
    theme = models.TextField(blank=True)
