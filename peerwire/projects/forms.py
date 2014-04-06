from django import forms
from django.forms import ModelForm
from projects.models import *

class UserLangForm(forms.ModelForm):
    class Meta:
        model = UserLang
        fields = ['lang', 'level']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['mail', 'first_name', 'last_name', 'description']

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'langs', 'skills', 'level', 'status',
            'seeking']

