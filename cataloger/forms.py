# Using Django forms
#
# More information is available here: https://docs.djangoproject.com/en/2.1/topics/forms/
#
# Also using ModelForms: https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/

from django import forms
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
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
                Submit('submit', 'Register', css_class='button white')
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

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['office'].queryset = Office.objects.filter(division_id=division_id).order_by('description')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Office queryset

class UploadBureauCodesCSVFileForm(forms.Form):
    file = forms.FileField()

class UploadDatasetsCSVFileForm(forms.Form):
    file = forms.FileField()

class NewDatasetForm(forms.Form):
    file = forms.FileField()
