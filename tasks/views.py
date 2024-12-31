from http.client import HTTPResponse
from lib2to3.fixes.fix_input import context

from django.http import HttpResponseRedirect
from django.shortcuts import render
from tasks.forms import TaskForm
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'tasks/index.html')
def erro404(request):
    return render(request, 'tasks/erro404.html')

@login_required()
def task(request, task_id):
        try:
         task = get_object_or_404(Task, id=task_id)
        except Http404 as exc:
            return HttpResponseRedirect(reverse('Erro404'))
        if task.user == request.user:
            context = {'task': task}
            return render(request, 'tasks/task.html', context)
        else:
            return HttpResponseRedirect(reverse('Erro404'))


@login_required()
def listarTasks(request):
    tipo=''
    status = request.GET.get('status')
    session = request.user
    if status == 'completed':
        tipo='completed'
        tasks = Task.objects.filter(completed=True, user=session.id)
    elif status == 'pending':
        tipo = 'pending'
        tasks = Task.objects.filter(completed=False, user=session.id)
    else:
        tipo = 'all'
        tasks = Task.objects.filter(user=session.id)

    context = {'tasks': tasks, 'tipo': tipo}
    return render(request, 'tasks/tasks.html', context)
@login_required()
def novaTask(request):
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('tasks'))

    context = {'form': form}

    return render(request, 'tasks/novatask.html', context)

@login_required()
def editTask(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)
    except Http404:
        return HttpResponseRedirect(reverse('Erro404'))

    if request.method != 'POST':
        form = TaskForm(instance=task)

    else:
        form = TaskForm(instance=task, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('task', args=[task.id]))


    context = {'form':form, 'task': task}

    return render(request, 'tasks/edit_task.html', context)


@login_required()
def deleteTask(request, task_id):
    try:
     task = get_object_or_404(Task, id=task_id)
    except Http404:
        return HttpResponseRedirect(reverse('Erro404'))
    task.delete()
    messages.success(request, "Tarefa deletada com sucesso!")
    return HttpResponseRedirect(reverse('tasks'))

@login_required()
def confirmDeleteTask(request, task_id):
    try:
     task = get_object_or_404(Task, id=task_id)
    except Http404:
        return HttpResponseRedirect(reverse('Erro404'))
    context={'task': task}
    return render(request, 'tasks/deleteTask.html', context)



