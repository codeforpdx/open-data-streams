# Using Django forms
#
# More information is available here: https://docs.djangoproject.com/en/2.1/topics/forms/
#
# Also using ModelForms: https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/

from django import forms
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div
from .models import BureauCode, Division, Office

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
                'Registration field set',
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
