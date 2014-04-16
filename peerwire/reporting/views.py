from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from reporting.models import *
from projects.models import Project, User
from projects.texts import report_done, report_p_failed, report_u_failed

def r_project(request, project_id):
    if not request.user.is_authenticated():
        return redirect('projects:index')
    project = get_object_or_404(Project, pk=project_id)
    qset = ProjectReport.objects.filter(project=project, made_by=request.user)
    if qset.count() < 1:
        r = ProjectReport(made_by=request.user, project=project)
        r.save()
        messages.success(request, report_done)
    else:
        messages.error(request, report_p_failed)
    return redirect('projects:projectpage', project.pk)

def r_user(request, user_id):
    if not request.user.is_authenticated():
        return redirect('projects:index')
    profile = get_object_or_404(User, pk=user_id)
    qset = UserReport.objects.filter(user=profile, made_by=request.user)
    if qset.count() < 1:
        r = UserReport(made_by=request.user, user=profile)
        r.save()
        messages.success(request, report_done)
    else:
        messages.error(request, report_u_failed)
    return redirect('projects:profilepage', profile.pk)

