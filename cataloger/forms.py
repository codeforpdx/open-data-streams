# Using Django forms
#
# More information is available here: https://docs.djangoproject.com/en/2.1/topics/forms/
#
# Also using ModelForms: https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/

from django import forms
from django.core import validators
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, HTML, Field
from crispy_forms.bootstrap import FormActions
from .models import BureauCode, Division, Office, Dataset, Distribution


class RegistrationForm(forms.ModelForm):
    """
    RegistrationForm is a Django ModelForm

    This form is used for the /registration page, and is rendered by the registration() fuction in views.py. The ModelForm is based off of the :model:`cataloger.models.Profile` class.

    Accepted Values:
        A request.POST dictionary (when filling existing form data), or None (when displaying a new/blank form)
    """
    password_confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Profile
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['username', 'first_name', 'last_name', 'password', 'email', 'bureau', 'division', 'office']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Create your OpenDataPDX Account',
                'username',
                'first_name',
                'last_name',
                'password',
                'password_confirm',
                'email',
                'bureau',
                'division',
                'office',
            ),
            ButtonHolder(
                Submit('submit', 'Register', css_class='btn btn-primary btn-sm btn-block')
            )
        )
        # set division and office selects to blank for initial bureau selection
        self.fields['division'].queryset = Division.objects.none()
        self.fields['office'].queryset = Office.objects.none()

        if 'bureau' in self.data:
            try:
                bureau_id = int(self.data.get('bureau'))
                self.fields['division'].queryset = Division.objects.filter(bureau_id=bureau_id).order_by('description')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Division queryset
        elif self.instance.pk:
            self.fields['division'].queryset = self.instance.bureau.division_set.order_by('description')

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['office'].queryset = Office.objects.filter(division_id=division_id).order_by('description')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Office queryset
        elif self.instance.pk:
            self.fields['office'].queryset = self.instance.division.office_set.order_by('description')

    # confirm passwords are the same
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self._errors["password_confirm"] = self.error_class(["Passwords do not match"])


class UploadBureauCodesCSVFileForm(forms.Form):
    """
    UploadBureauCodesCSVFileForm is a standard Django Form

    This form is used on the /utilities page, and is rendered by the utilities() function in views.py

    Purpose:
        The form is used to import :model:`cataloger.models.BureauCode`, :model:`cataloger.models.Division`, and :model:`cataloger.models.Office` objects from a CSV file

    Accepted Values:
        None (this form only displays a new/blank form)
    """
    file = forms.FileField()


class UploadDatasetsCSVFileForm(forms.Form):
    """
    UploadDatasetsCSVFileForm is a standard Django Form

    This form is used on the /utilities page, and is rendered by the utilities() function in views.py

    Purpose:
        The form is used to import :model:`cataloger.models.Dataset` objects from a CSV file

    Accepted Values:
        None (this form only displays a new/blank form)
    """
    file = forms.FileField()


class UploadFileForm(forms.Form):
    """
    UploadFileForm is a standard Django Form

    This form is used on the /utilities page, and is rendered by the utilities() function in views.py

    Purpose:
        The form is used to import different models from a file

    Accepted Values:
        None (this form only displays a new/blank form)
    """
    file = forms.FileField()

class NewDatasetURLForm(forms.Form):
    url = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'URL'}))
    username = forms.CharField(label="Username", required=False)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(NewDatasetURLForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'url',
                Div(
                    Div('username', css_class='col-md-6'),
                    Div('password', css_class='col-md-6'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Submit('url_submit', 'Submit', css_class='btn btn-primary')
            )
        )

class ImportDatasetURLForm(forms.Form):
    url = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'URL'}))
    username = forms.CharField(label="Username", required=False)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(ImportDatasetURLForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'url',
                Div(
                    Div('username',css_class='col-md-6',),
                    Div('password',css_class='col-md-6',),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Submit('url_submit', 'Submit', css_class='btn btn-primary')
            )
        )


class NewDatasetFileForm(forms.Form):
    file = forms.FileField(label="", required=True)



class ImportDatasetFileForm(forms.Form):
    file = forms.FileField(label="",required=True)

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['publisher', 'schema', 'mtype', 'title', 'description', 'keyword', 'identifier', 'accessLevel',
                  'bureauCode', 'programCode', 'license', 'spatial', 'temporal', 'describedByType', 'describedBy',
                  'accrualPeriodicity', 'conformsTo', 'dataQuality', 'isPartOf', 'issued', 'language', 'landingPage',
                  'primaryITInvestment', 'references', 'systemOfRecords', 'theme', 'published', ]
        widgets = {
            'publisher': forms.HiddenInput(),
            'schema': forms.HiddenInput(),
            'mtype': forms.HiddenInput(),
            'title': forms.TextInput(),
            'description': forms.TextInput(),
            'spatial': forms.TextInput(),
            'temporal': forms.TextInput(),
            'describedByType': forms.TextInput(),
            'describedBy': forms.TextInput(),
            'accrualPeriodicity': forms.TextInput(),
            'conformsTo': forms.TextInput(),
            'isPartOf': forms.TextInput(),
            'issued': forms.TextInput(),
            'landingPage': forms.TextInput(),
            'primaryITInvestment': forms.TextInput(),
            'systemOfRecords': forms.TextInput(),
            'published': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'publisher',
                'schema',
                'mtype',
                Field('title', css_class='form-control-lg', title='Human-readable name of the asset. Should be in plain English and include sufficient detail to facilitate search and discovery.'),
                Field('description', title='Human-readable description (e.g., an abstract) with sufficient detail to enable a user to quickly understand whether the asset is of interest.'),
                FormActions(HTML("""<a role="button" class="btn btn-primary m-3{% if distribution_id == -1 %} d-none{% endif %}" href= "{% if distribution_id != -1 %}{% url 'cataloger:distribution' distribution_id %}{% endif %}" > Edit Distribution </a>"""),
                            HTML("""<a role="button" class="btn btn-primary m-3{% if schema_id == -1 %} d-none{% endif %}" href= "{% if schema_id != -1 %}{% url 'cataloger:schema' schema_id %}{% endif %}" > Edit Schema </a>""")),
                Field('keyword', title='Tags (or keywords) help users discover your dataset; please include terms that would be used by technical and non-technical users.'),
                Field('identifier', title='A unique identifier for the dataset or API as maintained within an Agency catalog or database.'),
                Field('accessLevel', title='The degree to which this dataset could be made publicly-available, regardless of whether it has been made available'),
                Field('bureauCode', title=''),
                Field('programCode', title=''),
                Field('license',
                      title='The license or non-license (i.e. Public Domain) status with which the dataset or API has been published.'),
                Field('language', title=''),
                Field('spatial',
                      title='The range of spatial applicability of a dataset. Could include a spatial region like a bounding box or a named place.'),
                Field('temporal',
                      title='The range of temporal applicability of a dataset (i.e., a start and end date of applicability for the data).'),
                Field('describedByType',
                      title='The machine-readable file format (IANA Media Type also known as MIME Type) of the dataset’s Data Dictionary (describedBy).'),
                Field('describedBy', title='URL to the data dictionary for the dataset (taxonomies and ontologies).'),
                Field('accrualPeriodicity', title='The frequency with which dataset is published.'),
                Field('conformsTo',
                      title='URI used to identify a standardized specification the distribution conforms to.'),
                Field('dataQuality', title='Whether the dataset meets the agency’s Information Quality Guidelines.'),
                Field('isPartOf', title='The collection of which the dataset is a subset.'),
                Field('issued', title='Date of formal issuance.'),
                Field('landingPage',
                      title='This field is not intended for an agency’s homepage (e.g. www.agency.gov), but rather if a dataset has a human-friendly hub or landing page that users can be directed to for all resources tied to the dataset.'),
                Field('primaryITInvestment',
                      title='For linking a dataset with an IT Unique Investment Identifier (UII).'),
                Field('references',
                      title='Related documents such as technical information about a dataset, developer documentation, etc.'),
                Field('systemOfRecords',
                      title='If the system is designated as a system of records under the Privacy Act of 1974, provide the URL to the System of Records Notice related to this dataset.'),
                Field('theme', title='Main thematic category of the dataset.'),
                Field('published', title='Ticking this will make this asset visible to the public.'),
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-primary btn-sm btn-block'),
                HTML("""<a role="button" class="btn btn-block" href="{% url 'cataloger:dashboard' %}"> Cancel </a>""")
            )
        )


class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['accessURL', 'conformsTo', 'describedBy', 'describedByType', 'description', 'downloadURL', 'dformat',
                  'mediaType', 'title', ]
        widgets = {
            'accessURL': forms.TextInput(),
            'conformsTo': forms.TextInput(),
            'describedBy': forms.TextInput(),
            'describedByType': forms.TextInput(),
            'description': forms.TextInput(),
            'downloadURL': forms.TextInput(),
            'dformat': forms.TextInput(),
            'mediaType': forms.TextInput(),
            'title': forms.TextInput(),
        }
        labels = {
            'dformat': 'Format',
        }

    def __init__(self, *args, **kwargs):
        super(DistributionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('title', css_class="form-control-lg", title='Human-readable name of the distribution.'),
                Field('description', title='Human-readable description of the distribution.'),
                Field('downloadURL', title='URL providing direct access to a downloadable file of a dataset.'),
                Field('mediaType', title='The machine-readable file format (IANA Media Type or MIME Type) of the distribution’s downloadURL.'),
                Field('accessURL', title='URL providing indirect access to a dataset, for example via API or a graphical interface.'),
                Field('conformsTo', title='URI used to identify a standardized specification the distribution conforms to.'),
                Field('describedBy', title='URL to the data dictionary for the distribution found at the downloadURL. Note that documentation other than a data dictionary can be referenced using Related Documents as shown in the expanded fields.'),
                Field('describedByType', title='The machine-readable file format (IANA Media Type or MIME Type) of the distribution’s describedBy URL.'),
                Field('dformat', title='A human-readable description of the file format of a distribution.'),
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-primary btn-sm btn-block')
            )
        )


class SchemaForm(forms.Form):
    def __init__(self, json_data, title=None, type=None, *args, **kwargs):
        import json

        data = json.loads(json_data)

        super(SchemaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-primary')
            ),

            Fieldset(
                '',
                'title',
                'type',
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-primary')
            )
        )


        # choices for dropdown menu of types
        type_choices = [
            ('null', 'null'),
            ('boolean', 'boolean'),
            ('object', 'object'),
            ('array', 'array'),
            ('number', 'number'),
            ('string', 'string')
        ]
        #print("Got Schema data"+str(data))

        self.fields['type'] = forms.ChoiceField(choices=type_choices, required=False, label='Type', initial=2)
        self.initial['type'] = type

        self.fields['title'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control-lg', 'rows':1, 'cols':15}), required=False, initial = title)
        self.initial['title'] = title

        # Insert whole table here so that submit buttons can exist outside table
        self.helper.layout[1].extend([HTML("""
</br>
<table class='table'>
    <thead>
        <tr>
            <th scope='col'>Column</th>
            <th scope='col'>Description</th>
            <th scope='col'>Type</th>
        </tr>
    </thead>
<tbody>
        """)])

        # loop through data and append forms to layout
        for fields in data:
            name = fields['name']
            self.fields[name + "_description"] = forms.CharField(required=False, label='',
                                                                 initial=fields['description'])
            self.fields[name + "_type"] = forms.ChoiceField(choices=type_choices,
                                                            required=False, label='', initial=fields['type'])
            self.helper.layout[1].extend([
                HTML("<tr> <td>" + name + "</td> <td>"),
                Div(name + "_description"),
                HTML("</td> <td>"),
                Div(name + "_type"),
                HTML("</td> </tr>")
            ])

        self.helper.layout[1].extend([HTML('</tbody> </table>')])
