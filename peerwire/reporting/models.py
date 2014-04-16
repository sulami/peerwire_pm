from django.db import models

from projects.models import Project, User

class Report(models.Model):
    pub_date = models.DateField(auto_now_add=True)
    made_by = models.ForeignKey(User, related_name='%(class)s_made_by')

    class Meta:
        abstract = True

class ProjectReport(Report):
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.made_by.username + ' -> ' + str(self.project)

class UserReport(Report):
    user = models.ForeignKey(User, related_name='user')

    def __unicode__(self):
        return self.made_by.username + ' -> ' + self.user.username

