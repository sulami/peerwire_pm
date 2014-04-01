# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from projects.models import *
from news.models import News

def index(request):
    trending_projects = Project.objects.all().order_by('-value')[:10]
    news = News.objects.all().order_by('-pub_date')[:10]
    context = {
        'trending_projects': trending_projects,
        'news': news,
        }
    return render(request, 'projects/index.html', context)

def projectpage(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.status == 1:
        project.value += 1
        project.save()
    context = {'project': project}
    return render(request, 'projects/projectpage.html', context)

def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user not in project.owners.all():
        return redirect('projects:projectpage', project.pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:projectpage', project.pk)
    else:
        form = ProjectForm(instance=project)
    context = {'form': form, 'project': project}
    return render(request, 'projects/edit_project.html', context)

def startwork(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.seeking == 'Yes' and request.user not in project.users.all():
        project.users.add(request.user)
    return redirect('projects:projectpage', project.pk)

def finishwork(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user in project.users.all():
        project.users.remove(request.user)
    return redirect('projects:projectpage', project.pk)

def profilepage(request, profile_id):
    profile = get_object_or_404(User, pk=profile_id)
    context = {'profile': profile}
    return render(request, 'projects/profilepage.html', context)

def edit_profile(request):
    profile = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('projects:profilepage', profile.pk)
    else:
        form = UserForm(instance=profile)
    return render(request, 'projects/edit_profile.html', {'form': form})

