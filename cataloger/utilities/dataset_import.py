import csv
from cataloger.models import Profile, Dataset, Distribution, Schema, BureauCode, Division, Office
from datetime import datetime
import json, re, logging

# Datasets have these column headers:
# accessLevel,bureauCode,fn,hasEmail,description,downloadURL,mediaType,identifier,keyword,modified,programCode,publisher,title

def dataset_import(csvfile):
    decoded_file = csvfile.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    for row in reader:
        # All three of these must exist for new objects
        dataset = Dataset()
        distribution = Distribution()
        schema = Schema()
        
        # Create the schema
        schema.data = json.loads('{"test":"test"}')
        schema.save()
        dataset.schema = schema
        
        # Create the distribution, and populate its download URL from this data
        distribution.downloadURL = row['downloadURL']
        distribution.save()

        # Create the dataset
        dataset.distribution = distribution
        dataset.save()
        
        # Get a profile if it exists. If not, create a new one
        email = re.sub('mailto:', '', row['hasEmail'])
        profile = Profile.objects.filter(email=email).first()
        if profile is None:
            logging.error("Creating user...")
            # this email or Profile doesn't exist in the DB,
            # create a new profile
            profile = Profile()
            profile.email = email
            profile.username = email
            profile.first_name = row['fn'].split(' ')[0]
            if len(row['fn'].split(' ')) > 1:
                profile.last_name = row['fn'].split(' ')[1] #danger[!]
            profile.save()
        else:
            logging.error("Linking existing user...")
        dataset.publisher.add(profile)
        
        # Set the rest of the (mostly text) fields of the dataset
        dataset.accessLevel = row['accessLevel']
        dataset.bureauCode = row['bureauCode']
        dataset.description = row['description']
        dataset.mediaType = row['mediaType']
        dataset.identifier = row['identifier']
        dataset.keyword = row['keyword']
        dataset.modified = datetime.strptime(row['modified'], '%Y-%m-%dT%H:%M:%SZ')
        dataset.programCode = row['programCode']
        dataset.title = row['title']
        
        # Extended fields?
        dataset.accrualPeriodicity = row['accrualPeriodicity']
        dataset.conformsTo = row['conformsTo']
        dataset.dataQuality = row['dataQuality']
        dataset.issued = datetime.strptime(row['issued'], '%Y-%m-%d')
        dataset.landingPage = row['landingPage']
        dataset.language = row['language']
        dataset.primaryITInvestmentUII = row['primaryITInvestmentUII']
        dataset.references = row['references']
        dataset.rights = row['rights']
        dataset.spatial = row['spatial']
        dataset.systemOfRecords = row['systemOfRecords']
        dataset.temporal = row['temporal']
        dataset.theme = row['theme']
        dataset.isPartOf = row['isPartOf']

        
        dataset.save()

