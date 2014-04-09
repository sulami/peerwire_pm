from django.shortcuts import render

def index(request):
    return render(request, 'help/index.html')

def markdown(request):
    return render(request, 'help/markdown.html')

def projects(request):
    return render(request, 'help/projects.html')

