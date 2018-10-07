from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser

from .managers import ProfileManager

# City bureau codes, divisions, and offices
class BureauCode(models.Model):
    code = models.TextField()
    description = models.TextField(null=True)
    
    def __str__(self):
        return self.description

class Division(models.Model):
    bureau = models.ForeignKey(BureauCode, on_delete=models.CASCADE)
    division = models.TextField()
    description = models.TextField(null=True)
    
    def __str__(self):
        return self.description

class Office(models.Model):
    bureau = models.ForeignKey(BureauCode, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    office = models.TextField()
    description = models.TextField(null=True)

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
    mtype = models.TextField()
    accessURL = models.TextField()
    conformsTo = models.TextField()
    describedBy = models.TextField()
    describedByType = models.TextField()
    description = models.TextField()
    downloadURL = models.TextField()
    # format field (renamed since format is a reserved Python keyword)
    dformat = models.TextField()
    mediaType = models.TextField()
    title = models.TextField()

class Dataset(models.Model):
    # ---------- FOREIGN KEYS ----------
    # Relates a dataset to the user that published it.
    publisher = models.ManyToManyField(Profile)
    # Relates a dataset to its distribution.
    distribution = models.OneToOneField(Distribution, on_delete=models.CASCADE)
    # Relates a dataset to its schema.
    schema = models.OneToOneField(Schema, on_delete=models.CASCADE)

    # ---------- DATASET FIELDS ----------
    # @type field (renamed since type is a reserved Python keyword)
    mtype = models.TextField()
    title = models.TextField()
    description = models.TextField()
    # Could be a string that is a comma separated list.
    keywords = models.TextField()
    modified = models.DateTimeField(auto_now_add=True)
    # Will store a unique hash/slug that will be used to identify this dataset.
    identifier = models.TextField()
    accessLevel = models.TextField()
    bureauCode = models.TextField()
    programCode = models.TextField()
    license = models.TextField()

    # If applicable.
    spatial = models.TextField()
    temporal = models.TextField()

    # contactPoint -- doesn't exist as a field of Dataset. Instead, use the publisher's info.
    # (although we might decide to include this as a field or do this differently)

    describedByType = models.TextField()
    # Will store an API url for this dataset's schema.
    describedBy = models.TextField()

    # All dataset fields below this comment are (tentatively) to remain empty for this project.
    accrualPeriodicity = models.TextField(null=True)
    conformsTo = models.TextField(null=True)
    dataQuality = models.TextField(null=True)
    isPartOf = models.TextField(null=True)
    issued = models.TextField(null=True)
    language = models.TextField(null=True)
    landingPage = models.TextField(null=True)
    primaryITInvestment = models.TextField(null=True)
    references = models.TextField(null=True)
    systemOfRecords = models.TextField(null=True)
    theme = models.TextField(null=True)
