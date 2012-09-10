import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from forms import EditUserForm, NewUserForm


@login_required
def index(request, queryset=None, as_json=False):
  if not request.user.is_superuser:
    return HttpResponseForbidden()
  queryset = queryset or User.objects.all()
  if as_json:
    users = []
    for user in queryset.all():
      users.append({
                k:str(v) for k,v in user.__dict__.items() if k is not '_state'})
    content = json.dumps(users)
    return HttpResponse(content, content_type='application/json')
  return render(request, 'users/list.jade', {'user_list': queryset})


def new(request, form=None):
  form = form or NewUserForm()
  return render(request, 'users/new.jade', {'form': form})


@login_required
def edit(request, username, form=None):
  user = get_object_or_404(User, username=username)
  if user != request.user and not request.user.is_superuser:
    return HttpResponseForbidden()
  form = form or EditUserForm(instance=user)
  return render(request, 'users/edit.jade', {'form': form})
  
  
def _create(request):
  form = NewUserForm(request.POST)
  if form.is_valid():
    new_user = form.save()
    messages.success(request, "New user created!")
    return redirect(new_user)
  return new(request, form)
  

@login_required
def _update(request, username):
  user = get_object_or_404(User, username=username)
  if user != request.user and not request.user.is_superuser:
    return HttpResponseForbidden()
  form = EditUserForm(request.POST)
  if form.is_valid():
    updated_user = form.save()
    messages.success(request, "User edit successful.")
    return redirect(updated_user)
  return edit(request, username, form)
  

def _show(request, username=None, as_json=False, queryset=None):
  queryset = queryset or User.objects.all()
  if not username:
    return index(request, queryset, as_json)
  user = get_object_or_404(queryset, username=username)
  if as_json:
    content = json.dumps({
                k:str(v) for k,v in user.__dict__.items() if k is not '_state'})
    return HttpResponse(content, content_type='application/json')  
  return render(request, 'users/show.jade', {'user': user})


@login_required
def _destroy(request, username):
  user = get_object_or_404(User, username=username)
  if user != request.user and not request.user.is_superuser:
    return HttpResponseForbidden()
  user.delete()
  messages.success(request, "User destroyed")
  return redirect('home')


def do(request, **kwargs):
  """Handle `show`, `create`, `update`, and `destroy` actions."""

  if request.method == 'POST':
    method = request.POST.get('_method', 'POST')
  else:
    method = request.method

  return {
    'get': _show,
    'post': _create,
    'put': _update,
    'delete': _destroy,
  }[method.lower()](request, **kwargs)
  