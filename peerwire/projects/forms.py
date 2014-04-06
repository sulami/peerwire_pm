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
        fields = ['username', 'mail', 'first_name', 'last_name', 'desc']

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'desc', 'langs', 'skills', 'level', 'status',
            'seeking']

