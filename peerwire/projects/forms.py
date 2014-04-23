from django.forms import ModelForm, BooleanField, CharField, Form, PasswordInput
from projects.models import *
from projects.texts import project_ph, user_ph

class UserLangForm(ModelForm):
    class Meta:
        model = UserLang
        fields = ['lang', 'level']
    delete = BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserLangForm, self).__init__(*args, **kwargs)
        self.fields['lang'].queryset = Lang.objects.all().order_by('name')

class UserSkillForm(ModelForm):
    class Meta:
        model = UserSkill
        fields = ['skill', 'level']
    delete = BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserSkillForm, self).__init__(*args, **kwargs)
        self.fields['skill'].queryset = Skill.objects.all().order_by('name')

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'description', 'avatar']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['placeholder'] = user_ph
        self.fields['email'].required = True

class PasswordForm(Form):
    old_pw = CharField(widget=PasswordInput)
    new_pw1 = CharField(widget=PasswordInput)
    new_pw2 = CharField(widget=PasswordInput)

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'langs', 'skills', 'level', 'status',
            'seeking']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Required'
        self.fields['description'].widget.attrs['placeholder'] = project_ph
        self.fields['langs'].queryset = Lang.objects.all().order_by('name')
        self.fields['skills'].queryset = Skill.objects.all().order_by('name')

class InputForm(Form):
    username = CharField(max_length=100)

