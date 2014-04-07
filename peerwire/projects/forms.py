from django import forms
from django.forms import ModelForm, BooleanField
from projects.models import *

class UserLangForm(forms.ModelForm):
    class Meta:
        model = UserLang
        fields = ['lang', 'level']
    delete = forms.BooleanField(required=False)

class UserSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ['skill', 'level']
    delete = forms.BooleanField(required=False)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['mail', 'first_name', 'last_name', 'description']

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'langs', 'skills', 'level', 'status',
            'seeking']

