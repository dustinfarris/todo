import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from forms import EditTaskForm, NewTaskForm
from models import Task
from users.decorators import http_basic_auth


@login_required
def index(request, as_json=False):
  queryset = Task.objects.filter(user=request.user)
  if as_json:
    tasks = []
    for task in queryset.all():
      tasks.append({
                k:str(v) for k,v in task.__dict__.items() if k is not '_state'})
    content = json.dumps(tasks)
    return HttpResponse(content, content_type='application/json')
  return render(request, 'tasks/list.jade', {'task_list': queryset})


@login_required
def new(request, form=None):
  task = Task(user=request.user)
  form = form or NewTaskForm(instance=task)
  return render(request, 'tasks/new.jade', {'form': form})


@login_required
def edit(request, pk, form=None):
  task = get_object_or_404(Task, pk=pk, user=request.user)
  form = form or EditTaskForm(instance=task)
  return render(request, 'tasks/edit.jade', {'form': form, 'task': task})
  
  
@http_basic_auth
@login_required
def _create(request):
  form = NewTaskForm(request.POST)
  if form.is_valid():
    new_task = form.save(commit=False)
    new_task.user = request.user
    new_task.save()
    messages.success(request, "New task created!")
    return redirect('tasks:index')
  return new(request, form)
  

@http_basic_auth
@login_required
def _update(request, pk):
  task = get_object_or_404(Task, pk=pk, user=request.user)
  form = EditTaskForm(request.POST, instance=task)
  if form.is_valid():
    updated_task = form.save()
    messages.success(request, "Task edit successful.")
    return redirect('tasks:index')
  return edit(request, pk, form)
  

@http_basic_auth
@login_required
def _show(request, pk=None, as_json=False):
  if not pk:
    return index(request, as_json)
  task = get_object_or_404(Task, pk=pk, user=request.user)
  if as_json:
    content = json.dumps({
                k:str(v) for k,v in task.__dict__.items() if k is not '_state'})
    return HttpResponse(content, content_type='application/json')  
  return render(request, 'tasks/show.jade', {'task': task})


@http_basic_auth
@login_required
def _destroy(request, pk):
  task = get_object_or_404(Task, pk=pk)
  if task.user != request.user and not request.user.is_superuser:
    return HttpResponseForbidden()
  task.delete()
  messages.success(request, "Task destroyed")
  return redirect('tasks:index')


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
  