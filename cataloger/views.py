from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from django.contrib.auth import authenticate, login
import django.db, random, string
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from urllib.parse import urlparse
import os, logging

from .models import Dataset, Distribution, Schema, Profile, BureauCode, Division, Office, Catalog
from .forms import RegistrationForm, UploadBureauCodesCSVFileForm, UploadDatasetsCSVFileForm, NewDatasetFileForm, NewDatasetURLForm, DatasetForm, DistributionForm, SchemaForm
from .utilities import bureau_import, dataset_import, file_downloader, schema_generator, import_languages

def index(request):
    """
    Display the main site page.

    **Template:**

    :template:`cataloger/templates/index.html`
    """
    return render(request, 'index.html')


@user_passes_test(lambda u: u.is_authenticated)
def dashboard(request):
    """
    Display a dashboard interface, allowing the user to select from a list of :model:`cataloger.Dataset` objects.

    **Context**

    ``datasets``
        A list of :model:`cataloger.Dataset` instances affiliated with this user.

    **Template:**

    :template:`cataloger/templates/dashboard.html`
    """
    datasets = list(Dataset.objects.filter(publisher = request.user.id))

    return render(request, 'dashboard.html', {'datasets' : datasets})


def register(request):
    """
    Display the registration page, allowing a user to register for an account.

    This page is based off of the **form**:`cataloger.forms.RegistrationForm`.

    **Context**

    ``form``
        An instance of the **form**:`cataloger.forms.RegistrationForm` instances.

    **Template:**

    :template:`cataloger/templates/register.html`
    """
    if request.method == "POST":
        # this is a POST request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'], BureauCode.objects.filter(id = request.POST['bureau']).first(), Division.objects.filter(id = request.POST['division']).first(), Office.objects.filter(id = request.POST['office']).first())
            profile.save()

            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                # maybe we should redirect to invalid login page?
                # this shouldn't happen, however
                raise django.db.InternalError('Could not authenticate user')
        else:
            # If the form isn't valid, it will pass the form errors
            # through to the render function that returns below
            pass
    else:
        # this is a GET request
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})


@user_passes_test(lambda u: u.is_superuser)
def utilities(request):
    """
    Display the utilities page, allowing a user to perform various functions.

    **Context**

    ``bureaucodes_form``
        An instance of the **form**:`cataloger.forms.UploadBureauCodesCSVFileForm` class/object.

    ``datasets_form``
        An instance of the **form**:`cataloger.forms.UploadDatasetsCSVFileForm` class/object.

    **Template:**

    :template:`cataloger/templates/utilities.html`
    """
    if request.method == "POST":
        # this is a POST request
        if 'import-bureaus' in request.POST:
            # Bureau import form submission
            bureaucodes_form = UploadBureauCodesCSVFileForm(request.POST, request.FILES)
            datasets_form = UploadDatasetsCSVFileForm()
            if bureaucodes_form.is_valid():
                if len(BureauCode.objects.all()) == 0:
                    bureau_import.bureau_import(request.FILES['file'])
                else:
                    bureaucodes_form.add_error('file', 'Bureau codes already exist. You must remove them before importing new codes')
            else:
                # invalid form - this should pass back through to the page (with errors attached?)
                pass
        elif 'delete-bureaus' in request.POST:
            # Bureau delete form submission
            BureauCode.objects.all().delete()
            return HttpResponseRedirect('/utilities/')
        elif 'import-datasets' in request.POST:
            # Dataset import form submission
            datasets_form = UploadDatasetsCSVFileForm(request.POST, request.FILES)
            bureaucodes_form = UploadBureauCodesCSVFileForm()
            if datasets_form.is_valid():
                    dataset_import.dataset_import(request.FILES['file'])
            else:
                # invalid form - this should pass back through to the page (with errors attached?)
                pass
        elif 'import-languages' in request.POST:
            # Languages import
            import_languages.import_languages()
            return HttpResponseRedirect('/utilities/')
    else:
        # this is a GET request
        bureaucodes_form = UploadBureauCodesCSVFileForm()
        datasets_form = UploadDatasetsCSVFileForm()
    return render(request, 'utilities.html', {'bureaucodes_form': bureaucodes_form, 'datasets_form': datasets_form})


def load_divisions(request):
    """
    Used to load divisions for the registration Division select field.

    This page is used via AJAX calls to retrieve a list of filtered Division objects,
    based on the current BureauCode selection on the registration page.

    **Context**

    ``divisions``
        A filtered list of :model:`cataloger.divisions` .

    **Template:**

    :template:`cataloger/templates/divisions_dropdown_list_options.html`
    """
    bureau_id = request.GET.get('bureau')
    divisions = Division.objects.filter(bureau=bureau_id).order_by('description')
    return render(request, 'divisions_dropdown_list_options.html', {'divisions': divisions})


def load_offices(request):
    """
    Used to load offices for the registration Office select field.

    This page is used via AJAX calls to retrieve a list of filtered Office objects,
    based on the current Division selection on the registration page.

    **Context**

    ``offices``
        A filtered list of :model:`cataloger.offices` .

    **Template:**

    :template:`cataloger/templates/offices_dropdown_list_options.html`
    """
    division_id = request.GET.get('division')
    offices = Office.objects.filter(division=division_id).order_by('description')
    return render(request, 'offices_dropdown_list_options.html', {'offices': offices})

@user_passes_test(lambda u: u.is_authenticated)
def new_dataset(request):
    """
    Display the new_dataset page, allowing a user to create a dataset from various sources.

    This page is based on the **form**:`cataloger.forms.NewDatasetURLForm` and **form**:'cataloger.forms.NewDatasetFileForm` forms.

    **Context**

    ``url_form``
        An instance of the **form**:`cataloger.forms.NewDatasetURLForm` class.

    ``file_form``
        An instance of the **form**:`cataloger.forms.NewDatasetFileForm` class.

    **Template:**

    :template:`cataloger/templates/new_dataset.html`
    """
    valid_extensions = schema_generator.SchemaGenerator.valid_extensions

    if request.method == "POST":
        created_schema = None
        url = request.POST.get('url')  # None if not found
        if 'url_submit' in request.POST:
            # creates the form from the request.
            url_form = NewDatasetURLForm(request.POST)
            file_form = NewDatasetFileForm()

            # Checks if the form is valid.
            if url_form.is_valid():
                # Grabs the url, username, and password.
                username = request.POST['username']
                password = request.POST['password']
                temp_file = None
                # Attempts to download the file using the URL.
                try:
                    temp_file = file_downloader.FileDownloader.download_temp(url, username, password)
                    created_schema = schema_generator.SchemaGenerator.build(temp_file, urlparse(url).path.split('?')[0])
                # If it raises an exception, it attached the exception as an error on the form.
                except file_downloader.FailedDownloadingFileException as e:
                    created_schema = None
                    url_form.add_error('url', str(e))
                except schema_generator.FailedCreatingSchemaException as e:
                    created_schema = None
                    url_form.add_error('url', str(e))
                # All of other exceptions are caught and handled.
                except Exception as e:
                    created_schema = None
                    url_form.add_error('url', 'An error occurred while downloading the file.')
                    # log the error to console so that it can be found somewhere
                    logging.error("url_form Exception:" + str(e))
                finally:
                    if temp_file is not None:
                        temp_file.close()
            else:
                # If the form isn't valid, it passed back the form.
                pass
        # File form was submitted
        elif 'file_submit' in request.POST:
            url_form = NewDatasetURLForm()
            file_form = NewDatasetFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                # If a file was submitted, it grabs the file and stores a reference.
                file = request.FILES['file']
                if not file.name.lower().endswith(valid_extensions):
                    file_form.add_error(None, 'The provided file is not a supported type.')
                else:
                    try:
                        created_schema = schema_generator.SchemaGenerator.build(file, file.name)
                    except Exception as e:
                        created_schema = None
                        file_form.add_error(None, str(e))
        elif 'blank_submit' in request.POST:
            created_schema = Schema()
            created_schema.data = ''

        # if a schema was created, we create a new dataset with the schema and a new distribution (blank or url)
        if created_schema is not None:
            # save the created schema
            created_schema.save()
            # create and save distribution
            distribution = Distribution()
            if url is not None:
                distribution.downloadURL = url
                distribution.title = os.path.basename(urlparse(url).path.split('?')[0])
                if distribution.title.endswith('json'):
                    distribution.mediaType = "application/json"
                elif distribution.title.endswith('csv'):
                    distribution.mediaType = "text/csv"
                elif distribution.title.endswith('xlsx'):
                    distribution.mediaType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            distribution.save()
            # create and saves a dataset.
            dataset = Dataset()
            dataset.schema = created_schema
            dataset.distribution = distribution
            profile = Profile.objects.get(id=request.user.id)
            dataset.publisher = profile
            dataset.save()
            # save in order to cross link to other models and populate the identifier
            if profile.bureau:
                dataset.bureauCode.add(profile.bureau)
            if profile.division:
                dataset.programCode.add(profile.division)
            # prepare path for dataset
            dataset_identifier_path = '/dataset/' + str(dataset.id)
            dataset.identifier = request.build_absolute_uri(dataset_identifier_path)
            dataset.save()
            return HttpResponseRedirect('/schema/'+str(dataset.id))
    else:
        url_form = NewDatasetURLForm()
        file_form = NewDatasetFileForm()

    return render(request, 'new_dataset.html', {'url_form': url_form, 'file_form': file_form, 'extensions': valid_extensions})

@user_passes_test(lambda u: u.is_authenticated)
def dataset(request, dataset_id=None):
    """
    Display the dataset ModelForm page, allowing a user to edit a dataset.

    This page is based off of the **form**:`cataloger.forms.DatasetForm`.

    **Context**

    ``dataset_id``
        An int value representing the ID of the current :model:`cataloger.Dataset` that is being edited.

    ``dataset_form``
        An instance of the **form**:`cataloger.forms.DatasetForm` class.

    **Template:**

    :template:`cataloger/templates/dataset.html`
    """
    ds = get_object_or_404(Dataset, id=dataset_id)
    if ds.publisher.id is not request.user.id:
        # the user doesn't own this distribution, don't allow access
        return HttpResponse('Forbidden', status=403)
    if request.method == "POST":
        dataset_form = DatasetForm(instance=ds, data=request.POST)
        # this is a POST request
        if dataset_form.is_valid():
            # the form is valid - save it
            dataset_form.save()
            return HttpResponseRedirect('/dashboard/')
        else:
            # add the errors to the form
            dataset_form.add_error(None, str(dataset_form.errors))
    else:
        # this is probably a GET request
        dataset_form = DatasetForm(instance=ds)
        dataset_form.fields['distribution'].queryset = Distribution.objects.filter(dataset=ds)

    return render(request, 'dataset.html', {'dataset_id':dataset_id, 'form':dataset_form})

@user_passes_test(lambda u: u.is_authenticated)
def distribution(request, distribution_id=None):
    """
    Display the distribution ModelForm page, allowing a user to edit a distribution.

    This page is based off of the **form**:`cataloger.forms.DistributionForm`.

    **Context**

    ``distribution_id``
        An int value representing the ID of the current :model:`cataloger.Distribution` that is being edited.

    ``distribution_form``
        An instance of the **form**:`cataloger.forms.DistributionForm` class.

    **Template:**

    :template:`cataloger/templates/distribution.html`
    """
    dn = get_object_or_404(Distribution, id=distribution_id)
    if dn.dataset.publisher.id is not request.user.id:
        # the user doesn't own this distribution, throw an HTTP unauthorized
        return HttpResponse('Unauthorized', status=401)

    if request.method == "POST":
        distribution_form = DistributionForm(instance=dn, data=request.POST)
        # this is a POST request
        if distribution_form.is_valid():
            # the form is valid - save it
            distribution_form.save()
            return HttpResponseRedirect('/dataset/' + str(distribution_id))
        else:
            # the return below will display form errors
            pass
    else:
        # this is probably a GET request
        distribution_form = DistributionForm(instance=dn)
    return render(request, 'distribution.html', {'distribution_id':distribution_id, 'form':distribution_form})

@user_passes_test(lambda u: u.is_authenticated)
def schema(request, schema_id=None):
    import json

    # validate that the slug exists and grab json blob
    try:
        dataset = Dataset.objects.get(id=schema_id)
    except ObjectDoesNotExist:
        raise Http404("Schema does not exist")
    data = dataset.schema.data
    data = json.loads(data)
    property_data = json.dumps(data["properties"])

    if request.method == 'POST':
        form = SchemaForm(property_data, data=request.POST)
        if form.is_valid():
            # loop over the property fields and pull the submitted data
            counter = 0
            for fields in data['properties']:
                name = fields["name"]
                data["properties"][counter]["type"] = request.POST[name+'_type']
                data["properties"][counter]["description"] = request.POST[name+'_description']
                counter += 1

            # the form is valid - save it
            dataset.schema.data = json.dumps(data)
            dataset.schema.save()
            return HttpResponseRedirect('/dataset/' + str(schema_id))
        else:
            # the return below will display form errors
            pass
    else:
        form = SchemaForm(property_data)

    return render(request, 'schema.html', {'schema_id':schema_id, 'form':form})


# REST Framework
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from .serializers import DatasetSerializer, CatalogSerializer

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    """
    View to list the catalog
    """
    if request.method == 'GET':
        _context = serializers.URLField(label='@context', initial='https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld')
        _id = serializers.URLField(label='@id')
        _type = serializers.CharField(label='@type', initial='dcat:Catalog')
        _conformsTo = serializers.URLField(label='@conformsTo', initial='https://project-open-data.cio.gov/v1.1/schema')
        describedBy = serializers.URLField(initial='https://project-open-data.cio.gov/v1.1/schema/catalog.json')
        dataset = Dataset.objects.all().first()
        
        catalog = Catalog(_context=_context, _id=_id, _type=_type, _conformsTo=_conformsTo, describedBy=describedBy, dataset=dataset)

        serializer = CatalogSerializer(catalog)
    return Response(serializer.data)

@permission_classes((permissions.AllowAny,))
class DatasetList(APIView):
    def get(self, request, dataset_id=None, format=None):
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

@permission_classes((permissions.AllowAny,))
class DatasetDetail(APIView):

    def get(self, request, dataset_id=None, format=None):
        dataset = get_object_or_404(Dataset, id=dataset_id)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
