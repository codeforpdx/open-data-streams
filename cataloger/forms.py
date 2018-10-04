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
        self.fields['division'].queryset = Division.objects.none()
        self.fields['office'].queryset = Office.objects.none()
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

class UploadCSVFileForm(forms.Form):
    file = forms.FileField()
