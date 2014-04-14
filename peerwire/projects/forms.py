from django.forms import ModelForm, BooleanField, CharField, Form
from projects.models import *

project_ph = """You can use Markdown here
 (http://daringfireball.net/projects/markdown/syntax). You also might want to
 include a way to contact the person responsible for this project, like an email
 address or an irc channel. This help text will not be in the description."""

class UserLangForm(ModelForm):
    class Meta:
        model = UserLang
        fields = ['lang', 'level']
    delete = BooleanField(required=False)

class UserSkillForm(ModelForm):
    class Meta:
        model = UserSkill
        fields = ['skill', 'level']
    delete = BooleanField(required=False)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'description', 'avatar']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'langs', 'skills', 'level', 'status',
            'seeking']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['placeholder'] = project_ph


class InputForm(Form):
    username = CharField(max_length=100)

