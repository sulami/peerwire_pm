from django.contrib import admin
from projects.models import Project, Worker, Lang, Skill

admin.site.register(Project)
admin.site.register(Worker)
admin.site.register(Lang)
admin.site.register(Skill)

