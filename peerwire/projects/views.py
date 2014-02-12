# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from projects.models import *

def index(request):
    trending_projects = Project.objects.all().order_by('-value')[:10]
    context = {'trending_projects': trending_projects}
    return render(request, 'projects/index.html', context)

def projectpage(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {'project': project}
    return render(request, 'projects/projectpage.html', context)
