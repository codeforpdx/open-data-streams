# Using Django forms
#
# More information is available here: https://docs.djangoproject.com/en/2.1/topics/forms/
#
# Also using ModelForms: https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/

from django import forms
from django.core import validators
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, HTML
from .models import BureauCode, Division, Office, Dataset, Distribution

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['username', 'password', 'email', 'bureau', 'division', 'office']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Create your OpenDataPDX Account',
                'username',
                'password',
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

class UploadBureauCodesCSVFileForm(forms.Form):
    file = forms.FileField()

class UploadDatasetsCSVFileForm(forms.Form):
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
    file = forms.FileField(label="",required=True)

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['publisher', 'distribution', 'schema', 'mtype', 'title', 'description', 'keywords', 'identifier', 'accessLevel', 'bureauCode', 'programCode', 'license', 'spatial', 'temporal', 'describedByType', 'describedBy', 'accrualPeriodicity', 'conformsTo', 'dataQuality', 'isPartOf', 'issued', 'language', 'landingPage', 'primaryITInvestment', 'references', 'systemOfRecords', 'theme',]
        widgets = {
          'title': forms.Textarea(attrs={'rows':1, 'cols':15}),
          'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'spatial': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'temporal': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'describedByType': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'describedBy': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'accrualPeriodicity': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'conformsTo': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'isPartOf': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'issued': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'landingPage': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'primaryITInvestment': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'references': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'systemOfRecords': forms.Textarea(attrs={'rows':4, 'cols':15}),
          'theme': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                'description',
                ButtonHolder(HTML("""<a role="button" class="btn btn-primary" href= "{% url 'distribution' dataset_id %}" > Edit Distribution </a>""")),
                HTML("<br>"), #TODO quick fix spacing the buttons for now
                ButtonHolder(HTML("""<a role="button" class="btn btn-primary" href= "#" > Edit Schema </a>""")),
                'keywords',
                'identifier',
                'accessLevel',
                'bureauCode',
                'programCode',
                'license',
                'language',
                'spatial',
                'temporal',
                'describedByType',
                'describedBy',
                'accrualPeriodicity',
                'conformsTo',
                'dataQuality',
                'isPartOf',
                'issued',
                'landingPage',
                'primaryITInvestment',
                'references',
                'systemOfRecords',
                'theme',
                ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-primary btn-sm btn-block')
            )
        )
        #if 'distribution' in self.fields:
                #self.fields['distribution'].widget.attrs['disabled'] = True
        #if 'schema' in self.fields:
                #self.fields['schema'].widget.attrs['disabled'] = True

class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['accessURL', 'conformsTo', 'describedBy', 'describedByType', 'description', 'downloadURL', 'dformat', 'mediaType', 'title',]
        widgets = {
          'accessURL': forms.Textarea(attrs={'rows':1, 'cols':15}),
          'conformsTo': forms.Textarea(attrs={'rows':1, 'cols':15}),
          'describedBy': forms.Textarea(attrs={'rows':1, 'cols':15}),
          'describedByType': forms.Textarea(attrs={'rows':1, 'cols':15}),
          'description': forms.Textarea(attrs={'rows':1, 'cols':15}),
          'downloadURL': forms.Textarea(attrs={'rows':1, 'cols':15}),
          'dformat': forms.Textarea(attrs={'rows':1, 'cols':15}),
          'mediaType': forms.Textarea(attrs={'rows':1, 'cols':15}),
          'title': forms.Textarea(attrs={'rows':1, 'cols':15}),
        }
    def __init__(self, *args, **kwargs):
        super(DistributionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'accessURL',
                'conformsTo',
                'describedBy',
                'describedByType',
                'description',
                'downloadURL',
                'dformat',
                'mediaType',
                'title',
                ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-primary btn-sm btn-block')
            )
        )

class SchemaForm(forms.Form):
    def __init__(self, json_data, *args, **kwargs):
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
            self.fields[name+"_description"] = forms.CharField(required=False, label='',
                                                               initial=fields['description'])
            self.fields[name+"_type"] = forms.ChoiceField(choices=type_choices,
                                                          required=False, label='', initial=fields['type'])
            self.helper.layout[1].extend([
                HTML("<tr> <td>"+name+"</td> <td>"),
                Div(name+"_description"),
                HTML("</td> <td>"),
                Div(name+"_type"),
                HTML("</td> </tr>")
            ])

        self.helper.layout[1].extend([HTML('</tbody> </table>')])
