from django.db import models
from django.contrib.auth.models import AbstractUser

# Global difficulty levels
LEVEL_CHOICES = (
    (0, 'Beginner'),
    (1, 'Easy'),
    (2, 'Medium'),
    (3, 'Advanced'),
    (4, 'Expert'),
)

# Get the full project path in the project tree
def get_project_path(p, b=''):
    b = p.name + b
    if p.parent:
        b = '/' + b
        return get_project_path(p.parent, b)
    else:
        return b

# Get the project tree with the current project as root, returns a dict with
# projects and level difference from root
def get_project_tree(p, tree, i=0):
    if p.project_set:
        tree[p] = i
        i += 1
        for sp in p.project_set.all():
            get_project_tree(sp, tree, i)
    else:
        tree[p] = i
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
    value = models.IntegerField(default=0)

    def project_tree(self):
        return get_project_tree(self, {})

    def project_root(self):
        return get_project_root(self, [])

    def __unicode__(self):
        return get_project_path(self)

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

