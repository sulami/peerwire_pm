from django.contrib import admin
from projects.models import Project, User, Lang, Skill

admin.site.register(Project)
admin.site.register(User)
admin.site.register(Lang)
admin.site.register(Skill)

