from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from functions import *

# Global difficulty levels
LEVEL_CHOICES = (
    ('Beginner', 'Beginner'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Advanced', 'Advanced'),
    ('Expert', 'Expert'),
)

class Lang(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True)
    description = models.TextField(blank=True)
    del_t = models.DateField(blank=True, null=True)
    premium = models.BooleanField(default=False)

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
    description = models.TextField(blank=True)
    langs = models.ManyToManyField(Lang, blank=True)
    users = models.ManyToManyField(
        User, related_name='projects_workingon', blank=True
        )
    level = models.CharField(
        max_length=8,
        choices=LEVEL_CHOICES,
        blank=False, default=''
        )
    STATUS_CHOICES = (
        ('Inactive', 'Inactive'),
        ('Active', 'Active'),
    )
    status = models.CharField(
        max_length= 8,
        choices=STATUS_CHOICES,
        blank=False, default='Active'
        )
    parent = models.ForeignKey('self', blank=True, null=True)
    SEEKING_CHOICES = (
        ('No', 'Not seeking for help'),
        ('Yes', 'Seeking for help'),
    )
    seeking = models.CharField(
        max_length=3,
        choices=SEEKING_CHOICES,
        blank=False, default='No'
        )
    value = models.IntegerField(default=0)
    pub_date = models.DateField(auto_now_add=True)
    change_date = models.DateField(auto_now=True)
    del_q = models.ManyToManyField(User, blank=True, related_name='del_q')
    del_t = models.DateField(blank=True, null=True)

    def project_tree(self):
        return get_project_tree(self, '', [], 0, 1)

    def project_root(self):
        return get_project_root(self, [])

    def __unicode__(self):
        return get_project_path(self)

class UserLang(models.Model):
    lang = models.ForeignKey(Lang)
    user = models.ForeignKey(User)
    level = models.CharField(max_length=8, choices=LEVEL_CHOICES)

    def __unicode__(self):
        return self.lang.name

class Credit(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    ack = models.IntegerField(default=0)

