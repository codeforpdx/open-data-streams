import csv
from cataloger.models import Profile, Dataset, Distribution, Schema, BureauCode, Division, Office, AccessLevel, Keyword, Language, Catalog, References, Theme
from datetime import datetime
import json, re
from django.core.exceptions import ObjectDoesNotExist

# Datasets have these column headers:
# accessLevel,bureauCode,fn,hasEmail,description,downloadURL,mediaType,identifier,keyword,modified,programCode,publisher,title

def dataset_import_csv(csvfile):
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
        
        # Get a profile if it exists. If not, create a new one
        email = re.sub('mailto:', '', row['hasEmail'])
        profile = Profile.objects.filter(email=email).first()
        if profile is None:
            # this email or Profile doesn't exist in the DB,
            # create a new profile
            profile = Profile()
            profile.email = email
            profile.username = email
            profile.first_name = row['fn'].split(' ')[0]
            if len(row['fn'].split(' ')) > 1:
                profile.last_name = row['fn'].split(' ')[1] #danger[!]
            profile.save()
        dataset.publisher = profile
 
        # Create the dataset
        dataset.distribution = distribution
        dataset.save()
        
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

def dataset_import_json(jsonfile):
    # Decode the catalog dictionary from the JSON file being imported
    catalog = json.load(jsonfile)
    # This file may have several datasets specified - iterate over them
    for ds in catalog['dataset']:
        # There should only be a single catalog instance - retrieve it
        try:
            catalog = Catalog.objects.get(id=1)
        except ObjectDoesNotExist:
            catalog = Catalog()
            catalog.save()
            
        # Create a new dataset
        dataset = Dataset()
        # Assign this dataset to the main catalog
        dataset.catalog = catalog
        
        # Create an empty schema (we aren't hosting the schemas for imported datasets)
        schema = Schema()
        schema.data = {}
        schema.save()
        # Assign the schema to this dataset
        dataset.schema = schema
        
        # Get a profile if it exists. If not, create a new one
        contactPoint = ds['contactPoint']
        email = re.sub('mailto:', '', contactPoint['hasEmail'])
        profile = Profile.objects.filter(email=email).first()
        if profile is None:
            # this email or Profile doesn't exist in the DB,
            # create a new profile
            profile = Profile()
            profile.email = email
            profile.username = email
            profile.first_name = contactPoint['fn'].split(' ')[0]
            if len(contactPoint['fn'].split(' ')) > 1:
                profile.last_name = contactPoint['fn'].split(' ')[1] #danger[!]
            profile.save()
        dataset.publisher = profile
        
        # Create the dataset
        dataset.save()
        
        # Create the distribution object for each one in this dataset,
        # and populate its fields from this distribution objects
        if 'distribution' in ds.keys():
            for dn in ds['distribution']:
                distribution = Distribution()
                for field in dn:
                    distribution.field = dn[field]
                distribution.save()
                distribution.dataset = dataset
        
        # Set the rest of the fields of the dataset
        
        # AccessLevel
        try:
            accessLevel = AccessLevel.objects.get(accessLevel=ds['accessLevel'])
        except ObjectDoesNotExist:
            accessLevel = AccessLevel()
            accessLevel.accessLevel = ds['accessLevel']
            accessLevel.save()
        finally:
            dataset.accessLevel = accessLevel

        # BureauCode
        bureauCode = None
        for bc in ds['bureauCode']:
            try:
                bureauCode = BureauCode.objects.get(code=bc)
            except ObjectDoesNotExist:
                bureauCode = BureauCode()
                bureauCode.code = bc
                bureauCode.description = bc
                bureauCode.save()
            finally:
                dataset.bureauCode.add(bureauCode)

        # ProgramCode
        for pc in ds['programCode']:
            try:
                programCode = Division.objects.get(division=pc)
            except ObjectDoesNotExist:
                programCode = Division()
                programCode.division = pc
                programCode.bureau = bureauCode
                programCode.description = pc
                programCode.save()
            finally:
                dataset.programCode.add(programCode)
            
        # Keyword
        for kw in ds['keyword']:
            try:
                keyword = Keyword.objects.get(keyword=kw)
            except ObjectDoesNotExist:
                keyword = Keyword()
                keyword.keyword = kw
                keyword.save()
            finally:
                dataset.keyword.add(keyword)

        # Language
        if 'language' in ds.keys():
            for lg in ds['language']:
                try:
                    language = Language.objects.get(language=lg)
                except ObjectDoesNotExist:
                    language = Language()
                    language.language = lg
                    language.description = lg
                    language.save()
                finally:
                    dataset.language.add(language)

        # Additional text (non-model) fields
        if 'description' in ds.keys():
            dataset.description = ds['description']
        if 'mediaType' in ds.keys():
            dataset.mediaType = ds['mediaType']
        if 'identifier' in ds.keys():
            dataset.identifier = ds['identifier']
        if 'modified' in ds.keys():
            dataset.modified = datetime.strptime(ds['modified'], '%Y-%m-%dT%H:%M:%SZ')
        if 'title' in ds.keys():
            dataset.title = ds['title']
        
        # Extended fields?
        if 'accrualPeriodicity' in ds.keys():
            dataset.accrualPeriodicity = ds['accrualPeriodicity']
        if 'confirmsTo' in ds.keys():
            dataset.conformsTo = ds['conformsTo']
        if 'dataQuality' in ds.keys():
            dataset.dataQuality = ds['dataQuality']
        if 'issued' in ds.keys():
            dataset.issued = datetime.strptime(ds['issued'], '%Y-%m-%d')
        if 'landingPage' in ds.keys():
            dataset.landingPage = ds['landingPage']
        if 'primaryITInvestmentUII' in ds.keys():
            dataset.primaryITInvestmentUII = ds['primaryITInvestmentUII']
        if 'references' in ds.keys():
            for rf in ds['references']:
                try:
                    print("Got reference:"+str(rf))
                    reference = References.objects.get(reference=rf)
                except ObjectDoesNotExist:
                    print("Creating reference...")
                    reference = References()
                    reference.reference = rf
                    reference.save()
                finally:
                    dataset.references.add(reference)
        if 'rights' in ds.keys():
            dataset.rights = ds['rights']
        if 'spatial' in ds.keys():
            dataset.spatial = ds['spatial']
        if 'systemOfRecords' in ds.keys():
            dataset.systemOfRecords = ds['systemOfRecords']
        if 'temporal' in ds.keys():
            dataset.temporal = ds['temporal']
        if 'theme' in ds.keys():
            for th in ds['theme']:
                try:
                    theme = Theme.objects.get(theme=th)
                except ObjectDoesNotExist:
                    theme = Theme()
                    theme.theme = th
                    theme.save()
                finally:
                    dataset.theme.add(theme)
        if 'isPartOf' in ds.keys():
            dataset.isPartOf = ds['isPartOf']

        dataset.save()
