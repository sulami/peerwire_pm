# coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser

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

# This function makes a list of lists, containing a projects object and some
# HTML-code for the tree-style display, using unicode and an unhealthy amount of
# values passed in loops.
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
    mail = models.EmailField()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.mail], **kwargs)

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
    langs = models.ManyToManyField(Lang)
    skills = models.ManyToManyField(Skill)
    users = models.ManyToManyField(
        User, related_name='projects_workingon', blank=True
        )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        blank=False, default=''
        )
    STATUS_CHOICES = (
        ('Inactive', 'Inactive'),
        ('Active', 'Active'),
    )
    status = models.CharField(
        max_length= 10,
        choices=STATUS_CHOICES,
        blank=False, default=''
        )
    parent = models.ForeignKey('self', blank=True, null=True)
    SEEKING_CHOICES = (
        ('No', 'Not seeking for help'),
        ('Yes', 'Seeking for help'),
    )
    seeking = models.CharField(
        max_length=3,
        choices=SEEKING_CHOICES,
        blank=False, default=''
        )
    value = models.IntegerField(default=0)

    def project_tree(self):
        return get_project_tree(self, '', [], 0, 1)

    def project_root(self):
        return get_project_root(self, [])

    def __unicode__(self):
        return get_project_path(self)

class UserLang(models.Model):
    lang = models.ForeignKey(Lang)
    user = models.ForeignKey(User)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    def __unicode__(self):
        return self.lang.name

class UserSkill(models.Model):
    skill = models.ForeignKey(Skill)
    user = models.ForeignKey(User)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    def __unicode__(self):
        return self.lang.name

class MetaLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200)

class Credit(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    ack = models.IntegerField(default=0)

