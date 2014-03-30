# coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm

# Global difficulty levels
LEVEL_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Advanced', 'Advanced'),
    ('Expert', 'Expert'),
)

# Get the full project path in the project tree
def get_project_path(p, b=''):
    b = p.name + b
    if p.parent:
        b = '/' + b
        return get_project_path(p.parent, b)
    else:
        return b

# This thing is so ugly. It makes a list of lists, containing a projects object
# and some HTML-code for the tree-style display, using unicode and an unhealthy
# amount of values passed in loops. But it seems to match the output of UNIX
# tree in every situation.
def get_project_tree(p, padding, tree, c, initial):
    if p.project_set:
        tree.append([ [p, padding] ])
        if p.parent and initial > 1:
            if c != p.parent.project_set.all().count():
                padding = padding[:-1] + u'│'
            else:
                padding = padding[:-1] + '&nbsp;'
        count = 0
        for sub in p.project_set.all().order_by('-value'):
            count += 1
            if count == p.project_set.all().count():
                get_project_tree(sub, padding + u'└', tree, count, initial + 1)
            else:
                get_project_tree(sub, padding + u'├', tree, count, initial + 1)
    else:
        tree.append([ [p, padding] ])
        return tree
    return tree

def get_project_root(p, tree):
    if p.parent:
        tree.insert(0, p.parent)
        get_project_root(p.parent, tree)
    return tree

class Lang(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True)
    desc = models.TextField(blank=True)

    def __unicode__(self):
        if self.first_name:
            if self.last_name:
                return self.username + ' - ' + self.get_full_name()
            else:
                return self.username + ' - ' + self.first_name
        else:
            return self.username

class Project(models.Model):
    name = models.CharField(max_length=50)
    owners = models.ManyToManyField(User, related_name='projects_owned')
    desc = models.TextField(blank=True)
    users = models.ManyToManyField(
        User, related_name='projects_workingon', blank=True
        )
    langs = models.ManyToManyField(Lang, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    STATUS_CHOICES = (
        ('Inactive', 'Inactive'),
        ('Active', 'Active'),
    )
    status = models.CharField(max_length= 10, choices=STATUS_CHOICES)
    parent = models.ForeignKey('self', blank=True, null=True)
    SEEKING_CHOICES = (
        ('No', 'Not seeking for help'),
        ('Yes', 'Seeking for help'),
    )
    seeking = models.CharField(max_length=3, choices=SEEKING_CHOICES)
    value = models.IntegerField(default=0)

    def project_tree(self):
        return get_project_tree(self, '', [], 0, 1)

    def project_root(self):
        return get_project_root(self, [])

    def __unicode__(self):
        return get_project_path(self)

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'desc', 'langs', 'skills', 'level', 'status',
            'seeking']

class UserSkill(models.Model):
    skill = models.ForeignKey(Skill)
    user = models.ForeignKey(User)
    level = models.IntegerField(choices=LEVEL_CHOICES)

    def __unicode__(self):
        return self.skill.name

class UserLang(models.Model):
    lang = models.ForeignKey(Lang)
    user = models.ForeignKey(User)
    level = models.IntegerField(choices=LEVEL_CHOICES)

    def __unicode__(self):
        return self.lang.name

class MetaLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200)

    class Meta:
        abstract = True

class UserLink(MetaLink):
    user = models.ForeignKey(User)

class ProjectLink(MetaLink):
    project = models.ForeignKey(Project)

class Credit(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    ack = models.IntegerField(default=0)

