from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login
import django.db, random, string
from django.contrib.auth.decorators import user_passes_test

from tempfile import TemporaryFile

from .models import Dataset, Distribution, Schema, Profile, BureauCode, Division, Office
from .forms import RegistrationForm, UploadBureauCodesCSVFileForm, UploadDatasetsCSVFileForm, NewDatasetFileForm, NewDatasetURLForm
from .utilities import bureau_import, dataset_import, file_downloader, schema_generator

def random_str(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(length))

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    datasets = None
    if request.user.is_authenticated:
      datasets = list(Dataset.objects.filter(publisher = request.user.id))
    else:
        datasets = []
        keys = [
            'title',
            'description',
            'tags',
            'modified',
            'publisher',
            'contactPoint',
            'accessLevel',
            'bureauCodeUSG',
            'programCodeUSG',
            'license',
        ]
        for i in range(1, 30):
            new_dataset = {}
            for key in keys:
                new_dataset[key] = random_str(5)
            datasets.append(new_dataset)

    return render(request, 'dashboard.html', {'datasets' : datasets})

def register(request):
    if request.method == "POST":
        # this is a POST request
        form = RegistrationForm(request.POST)
        if form.is_valid():
            import logging
            logging.error("POST data:" + str(request.POST))

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
    else:
        # this is a GET request
        bureaucodes_form = UploadBureauCodesCSVFileForm()
        datasets_form = UploadDatasetsCSVFileForm()
    return render(request, 'utilities.html', {'bureaucodes_form': bureaucodes_form, 'datasets_form': datasets_form})

def load_divisions(request):
    bureau_id = request.GET.get('bureau')
    divisions = Division.objects.filter(bureau=bureau_id).order_by('description')
    return render(request, 'divisions_dropdown_list_options.html', {'divisions': divisions})

def load_offices(request):
    division_id = request.GET.get('division')
    offices = Office.objects.filter(division=division_id).order_by('description')
    return render(request, 'offices_dropdown_list_options.html', {'offices': offices})

def new_dataset(request):
    if request.method == "POST":
        if 'url_submit' in request.POST:
            #creates the form from the request.
            url_form = NewDatasetURLForm(request.POST)
            file_form = NewDatasetFileForm()

            #Checks if the form is valid.
            if url_form.is_valid():
                #grabs the url
                url = request.POST['url']
                #it checks if the url ends with the file type that is supported.
                if(url.lower.endswith(('.csv','.xlsx','.json'))):
                    #checks if the string starts with http.
                    if(url.lower.startswith('https')):
                        #if it does, it tries to download the file using the https url.
                        temp_file = file_downloader(url)
                        #if is succeeds, it will generate the schema.
                        if(temp_file is not None):
                            created_schema = schema_generator(file,url)
                            #deallocates the temporary file by closing it.
                            temp_file.close()
                            return HttpResponseRedirect('/dashboard/')
                        else:
                            #otherwise, it failed to download the file.
                            url_form.add_error(url, 'The provided https file failed to be downloaded.')
                            pass
                    else:
                        #otherwise, it checks if the string starts with sftp.
                        if(url.lower.startswith('sftp')):
                            #if it does, it grabs the username and password from the form tries to download the file.
                            username = request.POST['sftp_username']
                            password = request.POST['sftp_password']
                            temp_file = file_downloader(url,username,password)
                            #if is succeeds, it will generate the schema.
                            if(temp_file is not None):
                                created_schema = schema_generator(file,url)
                                #deallocates the temporary file by closing it.
                                temp_file.close()
                                return HttpResponseRedirect('/dashboard/')
                            else:
                                #otherwise, it failed to download the file.
                                url_form.add_error(url, 'The provided sftp file failed to be downloaded.')
                                pass
                        else:
                            #otherwise, the url isn't a supported type.
                            url_form.add_error(url, 'The provided URL is neither a http nor sftp.')
                            pass
                else:
                    #the URL doesn't end with a supported file type.
                    url_form.add_error(url, 'The provided URL directs to an unsupported file type.')
                    pass
            else:
                #if the form isn't valid, it passed back the form.
                pass
        #file form was submitted
        elif 'file_submit' in request.POST:
            url_form = NewDatasetURLForm()
            file_form = NewDatasetFileForm(request.POST)
            if file_form.is_valid():
                #if a file was submitted it grabs the file and stores a reference.
                file = request.FILES['file']
                if not file.name.lower.endswith(('.csv','.xlsx','.json')):
                    file_form.add_error(url, 'The provided file isn not an accepted type.')
                    pass
                created_schema = schema_generator(file,file.name)
                return HttpResponseRedirect('/dashboard/')
    else:
        url_form = NewDatasetURLForm()
        file_form = NewDatasetFileForm()

    return render(request, 'new_dataset.html', {'url_form':url_form, 'file_form':file_form})
