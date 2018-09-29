# Using Django forms
#
# More information is available here: https://docs.djangoproject.com/en/2.1/topics/forms/
#
# Also using ModelForms: https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/

from django import forms
from .models import Profile

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'user.password': forms.PasswordInput(),
        }
        fields = ['username', 'password', 'email', 'department', 'office']
