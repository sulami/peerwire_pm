from django.db import models
from django.contrib.auth.models import AbstractUser

class Lang(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Worker(AbstractUser):
    # Full name, email, password, time registered and last login are in meta
    # class AbstractUser
    avatar = models.ImageField(upload_to='avatars', blank=True)
    desc = models.TextField(blank=True)
    langs = models.ManyToManyField(Lang, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.get_username() + self.get_full_name()

class Project(models.Model):
    name = models.CharField(max_length=50)
    owners = models.ManyToManyField(Worker)
    desc = models.TextField(blank=True)
    langs = models.ManyToManyField(Lang, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    LEVEL_CHOICES = (
        (0, 'Beginner'),
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Advanced'),
        (4, 'Expert'),
    )
    level = models.IntegerField(choices=LEVEL_CHOICES)
    STATUS_CHOICES = (
        (0, 'Inactive'),
        (1, 'Active'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES)

    class Link(models.Model):
        name = models.CharField(max_length=50)
        url = models.URLField(max_length=200)

    def __str__(self):
        return self.name

class Credit(models.Model):
    worker = models.ForeignKey(Worker)
    project = models.ForeignKey(Project)
    ack = models.IntegerField(default=0)

