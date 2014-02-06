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

"""
About the project system:
There are projects and subprojects. Projects contain subprojects for e.g.
coding, localization, design, etc. for easy distinction. Let's say, you want to
make a website. The backend is done, but you still need webdesigners. Make a
subproject 'Design' and a subproject 'Code', and set Design to seeking. This
way, webdesigners will find their way to your project, but coders won't. This
can also be used for specific tasks within complex projects like filesystems or
content management systems, e.g. implementing a specific feature or fixing a
bigger bug.
All projects can contain subprojects, creating gigantic trees of projects for
a fine granular control of tasks. On the technical side of things, subprojects
have a value for 'parent', which references the parent object (which might
reference another parent, and so on).
"""

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
    parent = models.ForeignKey('self', blank=True, null=True)
    SEEKING_CHOICES = (
        (0, 'Not seeking for help'),
        (1, 'Seeking for help'),
    )
    seeking = models.IntegerField(choices=SEEKING_CHOICES)

    def __str__(self):
        return self.name

class Link(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200)

    class Meta:
        abstract = True

class WorkerLink(Link):
    worker = models.ForeignKey(Worker)

class ProjectLink(Link):
    project = models.ForeignKey(Project)

class Credit(models.Model):
    worker = models.ForeignKey(Worker)
    project = models.ForeignKey(Project)
    ack = models.IntegerField(default=0)

