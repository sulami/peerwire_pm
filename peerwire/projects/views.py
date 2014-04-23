from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.contrib.auth.hashers import check_password, make_password

from projects.models import *
from news.models import News
from projects.forms import *
from projects.texts import *

import datetime
import markdown
import Image

def index(request):
    trending_projects = Project.objects.all().order_by('-value')[:5]
    news = News.objects.all().order_by('-pub_date')[:10]
    context = {
        'trending_projects': trending_projects,
        'news': news,
        }
    if request.user.is_authenticated():
        proper = Project.objects.filter(
            seeking='Yes',
            status='Active'
            ).exclude(users__in=[request.user,])
        userlangs = request.user.userlang_set.all().values('lang')
        r_langs = proper.filter(langs__in=userlangs).distinct()
        userskills = request.user.userskill_set.all().values('skill')
        r_skills = r_langs.filter(skills__in=userskills)
        context['recommended'] = r_skills.order_by('users')[:5]
    return render(request, 'projects/index.html', context)

def projectpage(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.status == 'Active':
        project.value += 1
        project.save()
    context = {
        'project': project,
        'desc': markdown.markdown(
            project.description,
            safe_mode='escape',
            output_format='html5',
            extensions=['codehilite(noclasses=true,pygments_style=friendly)']
            )
        }
    return render(request, 'projects/projectpage.html', context)

def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user not in project.owners.all():
        return redirect('projects:projectpage', project.pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, changes_saved)
            return redirect('projects:projectpage', project.pk)
    else:
        form = ProjectForm(instance=project)
    context = {'form': form, 'project': project}
    return render(request, 'projects/edit_project.html', context)

def manage_users(request, project_id, user_id=None):
    project = get_object_or_404(Project, pk=project_id)
    if request.user not in project.owners.all():
        return redirect('projects:projectpage', project.pk)
    if user_id:
        user = get_object_or_404(User, pk=user_id)
        if user in project.users.all():
            project.users.remove(user)
            messages.success(request, user_removed)
            return redirect('projects:manage_users', project.pk)
    context = {'project': project}
    return render(request, 'projects/manage_users.html', context)

def add_owner(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user not in project.owners.all():
        return redirect('projects:projectpage', project.pk)
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(
                    username=form.cleaned_data.get('username')
                    )
            except:
                messages.error(request, user_not_found)
                return redirect('projects:add_owner', project_id)
            if user not in project.owners.all():
                project.owners.add(user)
                request.user.save()
                messages.success(request, owner_added)
            else:
                messages.error(request, user_already_owner)
                return redirect('projects:add_owner', project_id)
            return redirect('projects:projectpage', project.pk)
    else:
        form = InputForm()
    context = {'form': form, 'project': project}
    return render(request, 'projects/add_owner.html', context)

def owner_resign(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user not in project.owners.all():
        return redirect('projects:projectpage', project.pk)
    if not project.owners.all().count() > 1:
        messages.error(request, last_owner)
        return redirect('projects:projectpage', project.pk)
    project.owners.remove(request.user)
    request.user.save()
    messages.success(request, owner_resigned)
    return redirect('projects:projectpage', project.pk)

def start_project(request, parent_id=None):
    if not request.user.is_authenticated():
        return redirect('auth_login')
    if request.method == 'POST':
        project = Project()
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            p = form.save(commit=False)
            p.save()
            if parent_id:
                par = get_object_or_404(Project, pk=parent_id)
                if request.user not in par.owners.all():
                    return redirect('projects:projectpage', par.pk)
                p.parent = par
                p.save()
            p.owners.add(request.user)
            form.save()
            messages.success(request, project_started)
            return redirect('projects:projectpage', project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/start_project.html', {'form': form})

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user not in project.owners.all():
        return redirect('projects:projectpage', project.pk)
    if request.method == 'POST':
        if request.POST.get('delete'):
            if project.owners.all().count() <= 1:
                project.delete()
                messages.success(request, del_p_complete)
                return redirect('projects:index')
            for o in project.owners.all():
                if o != request.user:
                    project.del_q.add(o)
                    project.del_t = (
                        datetime.date.today() + datetime.timedelta(days=7)
                    )
                    project.save()
                    o.email_user(
                        'Your project %s is queued for deletion' % project,
                        project_del % (
                            project,
                            str(reverse(
                                'projects:delete_p_confirm',
                                args=(project.pk,)
                            )),
                            str(reverse(
                                'projects:delete_p_abort',
                                args=(project.pk,)
                            )),
                            str(project.del_t)
                        )
                    )
            return redirect('projects:delete_p_timer', project.pk)
    return render(request, 'projects/confirmation.html', {'project': project})

def delete_p_timer(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/delete_timer.html', {'project': project})

def delete_p_confirm(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user in project.del_q.all():
        project.del_q.remove(request.user)
        if project.del_q.all().count() <= 0:
            project.delete()
            messages.success(request, del_p_complete)
        else:
            messages.success(request, del_p_confirm)
    return redirect('projects:index')

def delete_p_abort(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user in project.del_q.all():
        for u in project.del_q.all():
            project.del_q.remove(u)
        project.del_t = None
        project.save()
        messages.success(request, del_p_abort)
        return redirect('projects:projectpage', project.pk)
    return redirect('projects:index')

def startwork(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not request.user.is_authenticated():
        return redirect('projects:projectpage', project.pk)
    if ((project.seeking == 'Yes' or request.user in project.owners.all()) and
        request.user not in project.users.all()):
        project.users.add(request.user)
        project.save()
        messages.success(request, work_started)
    return redirect('projects:projectpage', project.pk)

def finishwork(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if not request.user.is_authenticated():
        return redirect('projects:projectpage', project.pk)
    if request.user in project.users.all():
        project.users.remove(request.user)
        project.save()
        messages.success(request, work_finished)
    return redirect('projects:projectpage', project.pk)

def profilepage(request, profile_id):
    profile = get_object_or_404(User, pk=profile_id)
    context = {
        'profile': profile,
        'desc': markdown.markdown(
            profile.description,
            safe_mode='escape',
            output_format='html5',
            extensions=['codehilite(noclasses=true,pygments_style=friendly)']
            )
        }
    return render(request, 'projects/profilepage.html', context)

def edit_profile(request):
    if not request.user.is_authenticated():
        return redirect('projects:index')
    profile = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if 'email' in form.changed_data:
                request.user.email_user(
                    'Your email address has been changed',
                    'Your email address has been changed to %s.' %
                        form.cleaned_data.get('email')
                    )
            form.save()
            if 'avatar' in form.changed_data and form.cleaned_data.get(
                'avatar'
                ):
                im = Image.open(profile.avatar.path)
                if im.size[0] < im.size[1]:
                    ratio = im.size[1] / float(im.size[0])
                    out = im.resize((100, int(100 * ratio)))
                elif im.size[0] > im.size[1]:
                    ratio = im.size[0] / float(im.size[1])
                    out = im.resize((int(100 * ratio), 100))
                else:
                    out = im.resize((100, 100))
                out.save(profile.avatar.path, im.format)
            messages.success(request, changes_saved)
            return redirect('projects:profilepage', profile.pk)
    else:
        form = UserForm(instance=profile)
        pw_form = PasswordForm()
    return render(request, 'projects/edit_profile.html', {
        'form': form,
        'pw_form': pw_form,
        })

def edit_password(request):
    if not request.user.is_authenticated():
        return redirect('projects:index')
    profile = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            if check_password(
                form.cleaned_data.get('old_pw'),
                request.user.password
                ):
                if form.cleaned_data.get(
                    'new_pw1') == form.cleaned_data.get('new_pw2'):
                    pw = make_password(form.cleaned_data.get('new_pw1'))
                    request.user.password = pw
                    request.user.save()
                    request.user.email_user('Your password has been changed', pw_changed)
                    messages.success(request, changes_saved)
                    return redirect('projects:profilepage', profile.pk)
                else:
                    messages.error(request, "New passwords did not match.")
            else:
                messages.error(request, "Old password does not match.")
    return redirect('projects:edit_profile')

def delete_profile(request, profile_id):
    if not request.user.is_authenticated():
        return redirect('projects:index')
    profile = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        if request.POST.get('delete'):
            profile.del_t = datetime.date.today() + datetime.timedelta(days=7)
            profile.save()
            profile.email_user(
                'Your account is queued for deletion',
                profile_del % (
                    str(reverse('projects:delete_u_abort', args=(profile.pk,))),
                    str(profile.del_t)
                    )
                )
            messages.success(request, del_u)
            return redirect('projects:profilepage', profile.pk)
    return render(request, 'projects/confirmation.html', {'profile': profile})

def delete_u_abort(request, profile_id):
    profile = get_object_or_404(User, pk=request.user.pk)
    if request.user != profile:
        return redirect('projects:index')
    profile.del_t = None
    profile.save()
    messages.success(request, del_u_abort)
    return redirect('projects:profilepage', profile.pk)

def edit_langs(request):
    if not request.user.is_authenticated():
        return redirect('projects:index')
    profile = get_object_or_404(User, pk=request.user.pk)
    LangFormSet = modelformset_factory(
        UserLang,
        form=UserLangForm,
        )
    if request.method == 'POST':
        formset = LangFormSet(
            request.POST,
            queryset=UserLang.objects.filter(user=request.user)
            )
        if formset.is_valid():
            for form in formset.forms:
                if form.has_changed():
                    instance = form.save(commit=False)
                    if form.cleaned_data.get('delete'):
                        instance.delete()
                    else:
                        instance.user = request.user
                        instance.save()
            messages.success(request, changes_saved)
            return redirect('projects:profilepage', profile.pk)
    else:
        formset = LangFormSet(
            queryset=UserLang.objects.filter(user=request.user)
            )
    return render(request, 'projects/edit_langs.html', {'form': formset})

def edit_skills(request):
    if not request.user.is_authenticated():
        return redirect('projects:index')
    profile = get_object_or_404(User, pk=request.user.pk)
    SkillFormSet = modelformset_factory(
        UserSkill,
        form=UserSkillForm,
        )
    if request.method == 'POST':
        formset = SkillFormSet(
            request.POST,
            queryset=UserSkill.objects.filter(user=request.user)
            )
        if formset.is_valid():
            for form in formset.forms:
                if form.has_changed():
                    instance = form.save(commit=False)
                    if form.cleaned_data.get('delete'):
                        instance.delete()
                    else:
                        instance.user = request.user
                        instance.save()
            messages.success(request, changes_saved)
            return redirect('projects:profilepage', profile.pk)
    else:
        form = SkillFormSet(
            queryset=UserSkill.objects.filter(user=request.user)
            )
    return render(request, 'projects/edit_skills.html', {'form': form})

@cache_page(60 * 60)
@vary_on_headers('Cookie')
def about_us(request):
    return render(request, 'about_us.html')

@cache_page(60 * 60)
@vary_on_headers('Cookie')
def contact(request):
    return render(request, 'contact.html')
