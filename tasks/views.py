from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def home(request):
    """
    A view to display the tasks to do and the completed tasks
    with the tasks due soonest at the top
    """

    to_do_tasks = Task.objects.filter(completed=False).order_by('due_date')
    done_tasks = Task.objects.filter(completed=True).order_by('-due_date')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm()

    context = {
        'to_do_tasks': to_do_tasks,
        'done_tasks': done_tasks,
        'form': form,
    }

    return render(request, 'tasks/index.html', context)


def delete_task(request, task_id):
    """Delete a specific task"""
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    return redirect('home')


def toggle_task(request, task_id):
    """Toggle task completion status"""
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.completed = not task.completed
        task.save()
    return redirect('home')


# Create your views here.