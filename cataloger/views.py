from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from django.contrib.auth import authenticate, login
import django.db, random, string
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from urllib.parse import urlparse
import os, logging


from .models import Dataset, Distribution, Schema, Profile, BureauCode, Division, Office, Keyword, Catalog, Language
from .forms import RegistrationForm, UploadBureauCodesCSVFileForm, UploadDatasetsCSVFileForm, NewDatasetFileForm, NewDatasetURLForm, ImportDatasetFileForm, ImportDatasetURLForm, DatasetForm, DistributionForm, SchemaForm, UploadFileForm
from .utilities import bureau_import, dataset_import, file_downloader, schema_generator, import_languages, keyword_import

def index(request):
    """
    Display the main site page.

    **Template:**

    :template:`cataloger/templates/index.html`
    """
    return render(request, 'index.html')


@user_passes_test(lambda u: u.is_authenticated)
def dashboard(request):
    import csv
    """
    Display a dashboard interface, allowing the user to select from a list of :model:`cataloger.Dataset` objects.

    **Context**

    ``datasets``
        A list of :model:`cataloger.Dataset` instances affiliated with this user.

    **Template:**

    :template:`cataloger/templates/dashboard.html`
    """
    if request.method == "POST":
        # this is a POST request
        if 'action_type' in request.POST:
            if 'selected' in request.POST:
                # there are some datasets selected - proceed
                if request.POST['action_type'] == 'delete':
                    for selectedDataset in request.POST.getlist('selected'):
                        Dataset.objects.get(id=selectedDataset).delete()
                elif request.POST['action_type'] == 'publish':
                    for selectedDataset in request.POST.getlist('selected'):
                        dataset = Dataset.objects.get(id=selectedDataset)
                        dataset.published = True
                        dataset.save()
                elif request.POST['action_type'] == 'unpublish':
                    for selectedDataset in request.POST.getlist('selected'):
                        dataset = Dataset.objects.get(id=selectedDataset)
                        dataset.published = False
                        dataset.save()
                elif request.POST['action_type'] == 'complete':
                    for selectedDataset in request.POST.getlist('selected'):
                        dataset = Dataset.objects.get(id=selectedDataset)
                        form = DatasetForm(instance=dataset)
                        if form.is_valid():
                            dataset.complete = True
                            dataset.save()
    else:
        # this is a GET request
        pass
        
    if request.user.is_superuser:
        datasets = list(Dataset.objects.all())
    else:
        datasets = list(Dataset.objects.filter(publisher = request.user.id))

    if request.GET.get('export'):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="datasets.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Title', 'Description', 'Tags', 'Last Modified', 'Publisher', 'Contact Point',
                         'Access Level', 'Bureau Code', 'Program Code', 'License'])
        for current_dataset in datasets: 
            writer.writerow([str(current_dataset.id), str(current_dataset.title), str(current_dataset.description),
                             ','.join(map(str, current_dataset.keyword.all())), str(current_dataset.modified),
                             str(current_dataset.publisher), str(current_dataset.publisher.email),
                             str(current_dataset.accessLevel), ','.join(map(str, current_dataset.bureauCode.all())),
                             ','.join(map(str, current_dataset.programCode.all())), str(current_dataset.license)])
        return response

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
            form.clean()
            profile = Profile.objects.create_user(request.POST['username'], request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], BureauCode.objects.filter(id = request.POST['bureau']).first(), Division.objects.filter(id = request.POST['division']).first(), Office.objects.filter(id = request.POST['office']).first())
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
            keywords_form = UploadFileForm()
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
            keywords_form = UploadFileForm()
            if datasets_form.is_valid():
                dataset_import.dataset_import_json(request.FILES['file'])
            else:
                # invalid form - this should pass back through to the page (with errors attached?)
                pass
        elif 'import-languages' in request.POST:
            # Languages import
            import_languages.import_languages()
            return HttpResponseRedirect('/utilities/')
        elif 'import-keywords' in request.POST:
            print("Import keywords...")
            # Keyword import form submission
            bureaucodes_form = UploadBureauCodesCSVFileForm()
            datasets_form = UploadDatasetsCSVFileForm()
            keywords_form = UploadFileForm(request.POST, request.FILES)
            if keywords_form.is_valid():
                print("Keywords form is valid...")
                if len(Keyword.objects.all()) == 0:
                    print("No keywords exist - proceeding...")
                    keyword_import.keyword_import_excel(request.FILES['file'])
                else:
                    print("Error keywords exist - you must remove them before importing")
                    keywords_form.add_error(None, 'Keywords codes already exist. You must remove them before importing new keywords')
            else:
                # invalid form - this should pass back through to the page (with errors attached?)
                pass
    else:
        # this is a GET request
        bureaucodes_form = UploadBureauCodesCSVFileForm()
        datasets_form = UploadDatasetsCSVFileForm()
        keywords_form = UploadFileForm()
    return render(request, 'utilities.html', {'bureaucodes_form': bureaucodes_form, 'datasets_form': datasets_form, 'keywords_form': keywords_form})


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
            created_schema.data = '{"title": null, "type": null, "properties": []}'

        # if a schema was created, we create a new dataset with the schema and a new distribution (blank or url)
        if created_schema is not None:
            # save the created schema
            created_schema.save()
            # get the catalog if it exists, otherwise, create it
            # there should be only 1 catalog
            try:
                catalog = Catalog.objects.get(id=1)
            except Catalog.DoesNotExist:
                catalog = Catalog()
                catalog.save()
            # create and saves a dataset.
            dataset = Dataset()
            dataset.schema = created_schema
            profile = Profile.objects.get(id=request.user.id)
            dataset.publisher = profile
            dataset.catalog = catalog
            # prepare path for schema (describedBy)
            dataset_schema_path = '/api/schema/' + str(dataset.schema.id)
            dataset.describedBy = request.build_absolute_uri(dataset_schema_path)
            dataset.describedByType = "application/json"
            dataset.save()
            # save in order to cross link to other models and populate the identifier
            if profile.bureau:
                dataset.bureauCode.add(profile.bureau)
            if profile.division:
                dataset.programCode.add(profile.division)
            # prepare path for dataset
            dataset_identifier_path = '/api/dataset/' + str(dataset.id)
            dataset.identifier = request.build_absolute_uri(dataset_identifier_path)
            dataset.language.set(Language.objects.filter(language='en-US'))
            dataset.save()
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
            distribution.dataset = dataset
            distribution.save()
            return HttpResponseRedirect('/schema/'+str(dataset.id))
    else:
        url_form = NewDatasetURLForm()
        file_form = NewDatasetFileForm()

    return render(request, 'new_dataset.html', {'url_form': url_form, 'file_form': file_form, 'extensions': valid_extensions})

@user_passes_test(lambda u: u.is_authenticated)
def import_dataset(request):
    import json
    if request.method == "POST":
        url = request.POST.get('url')  # None if not found
        json_file = None
        if 'url_submit' in request.POST:
            # creates the form from the request.
            url_form = ImportDatasetURLForm(request.POST)
            file_form = ImportDatasetFileForm()

            # Checks if the form is valid.
            if url_form.is_valid():
                if urlparse(url).path.split('?')[0].endswith('.json'):
                    # Grabs the url, username, and password.
                    username = request.POST['username']
                    password = request.POST['password']
                    # Attempts to download the file using the URL.
                    try:
                        json_file = file_downloader.FileDownloader.download_temp(url, username, password)
                    # If it raises an exception, it attached the exception as an error on the form.
                    except file_downloader.FailedDownloadingFileException as e:
                        url_form.add_error('url', str(e))
                    # All of other exceptions are caught and handled.
                    except Exception as e:
                        url_form.add_error('url', 'An error occurred while downloading the file.')
                        # log the error to console so that it can be found somewhere
                        logging.error("url_form Exception:" + str(e))
                else:
                    url_form.add_error('url', 'The url does not point to a JSON file.')
        # File form was submitted
        elif 'file_submit' in request.POST:
            url_form = ImportDatasetURLForm()
            file_form = ImportDatasetFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                # If a file was submitted, it grabs the file and stores a reference.
                file = request.FILES['file']
                if not file.name.lower().endswith('.json'):
                    file_form.add_error(None, 'The provided file is not a JSON file.')
                else:
                    json_file = file

        if json_file is not None:
            try:
                dataset_import.dataset_import_json(json_file)
                return HttpResponseRedirect('/dashboard/')
            except Exception as e:
                if 'url_submit' in request.POST:
                    url_form.add_error('url', 'The provided URL does not point to a valid POD 1.1 catalog.')
                else:
                    file_form.add_error(None, 'The provided file is not a valid POD 1.1 catalog.')
                logging.error("Failed to parse JSON file: " + str(e))
    else:
        url_form = ImportDatasetURLForm()
        file_form = ImportDatasetFileForm()

    return render(request, 'import_dataset.html', {'url_form': url_form, 'file_form': file_form, 'extensions': {'.json'}})


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

    if not request.user.is_superuser and ds.publisher.id is not request.user.id:
        # the user doesn't own this distribution, don't allow access
        return HttpResponse('Forbidden', status=403)
    if request.method == "POST":
        dataset_form = DatasetForm(instance=ds, data=request.POST)
        # this is a POST request
        if dataset_form.is_valid():
            # the form is valid - save it
            dataset_form.save()
            # mark the Dataset as complete, save it, and redirect to the dashboard
            ds.complete = True
            ds.save()
            return HttpResponseRedirect('/dashboard/')
        else:
            # add the errors to the form
            dataset_form.add_error(None, str(dataset_form.errors))
    else:
        # this is probably a GET request
        dataset_form = DatasetForm(instance=ds)
        if not ds.complete:
            messages.warning(request, 'Dataset incomplete - please fill out all required fields.')

    # if there aren't any distributions for this dataset, disable the Edit Dataset button
    if ds.distribution_set.count() > 0:
        distribution_id = ds.distribution_set.first().id
    else:
        distribution_id = -1

    # if we aren't hosting the schema for this dataset, disable the Edit Schema button
    if '$schema' in ds.schema.data:
        schema_id = ds.schema.id
    else:
        schema_id = -1
    return render(request, 'dataset.html', {'dataset_id':dataset_id, 'distribution_id':distribution_id, 'schema_id':schema_id, 'form':dataset_form})

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
    if not request.user.is_superuser and dn.dataset.publisher.id is not request.user.id:
        # the user doesn't own this distribution, throw an HTTP unauthorized
        return HttpResponse('Unauthorized', status=401)

    if request.method == "POST":
        distribution_form = DistributionForm(instance=dn, data=request.POST)
        # this is a POST request
        if distribution_form.is_valid():
            # the form is valid - save it
            distribution_form.save()
            return HttpResponseRedirect('/dataset/' + str(dn.dataset.id))
        else:
            # the return below will display form errors
            pass
    else:
        # this is probably a GET request
        distribution_form = DistributionForm(instance=dn)
    return render(request, 'distribution.html', {'form':distribution_form})

@user_passes_test(lambda u: u.is_authenticated)
def schema(request, schema_id=None):
    import json

    # validate that the slug exists and grab json blob
    schema = get_object_or_404(Schema, id=schema_id)

    data = schema.data
    data = json.loads(data)

    # empty dataset was uploaded, redirect to dataset
    if data["properties"] == []:
        return HttpResponseRedirect('/dataset/'+ str(schema.dataset.id))

    # set property_data to the JSON blob's "properties" field
    property_data = json.dumps(data["properties"])
    # set title to the JSON blob's "title" field
    #title = data['title']
    # set type to the JSON blob's "type" field
    type = data['type']
    title = data['title']
    if request.method == 'POST':
        form = SchemaForm(property_data, data=request.POST)
        if form.is_valid():
            data['title'] = request.POST['title']
            data['type'] = request.POST['type']
            # loop over the property fields and pull the submitted data
            counter = 0
            for fields in data['properties']:
                name = fields["name"]
                data["properties"][counter]["type"] = request.POST[name+'_type']
                data["properties"][counter]["description"] = request.POST[name+'_description']
                counter += 1

            # the form is valid - save it
            json_schema_url = 'http://json-schema.org/draft-07/schema #'
            schema_identifier = request.build_absolute_uri('/api/schema/' + str(schema.id))
            temporary_dictionary = {'$schema': json_schema_url, '$id': schema_identifier}
            temporary_dictionary.update(data)
            schema.data = json.dumps(temporary_dictionary)
            schema.save()
            return HttpResponseRedirect('/dataset/' + str(schema.dataset.id))
        else:
            # the return below will display form errors
            pass
    else:
        form = SchemaForm(property_data, title, type)

    return render(request, 'schema.html', {'schema_id':schema_id, 'form':form})
