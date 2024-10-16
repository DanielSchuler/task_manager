pasos proyecto DJango Task manager
-------------------------------------
******** Step 1: Create project and app
pip install django
django-admin startproject task_manager
cd task_manager
python manage.py startapp tasks

******** Step 2: Update Settings


INSTALLED_APPS = [
    ...
    'tasks',
]


******** Step 3: Set Up Your Models


from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


******** Step 4: Create Database Migrations


python manage.py makemigrations
python manage.py migrate


******** Step 5: Create a Superuser


python manage.py createsuperuser


******** Step 6: Start the Development Server

python manage.py runserver


******** Step 7: Create View and Templates


from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


******** Step 8: Configure URLs


In the app create a file named urls.py

from django.urls import path
from .views import task_list

urlpatterns = [
    path('', task_list, name='task_list'),
]


Include the app's URLs in your project's main urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),  # Add this line
]


******** Step 10: Create Template


1) Create a directory named templates inside the tasks app directory.
Then create another directory named tasks within it.

2) Create a file named task_list.html inside tasks/templates/tasks/
with the following content:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task List</title>
</head>
<body>
    <h1>Task List</h1>
    <ul>
        {% for task in tasks %}
            <li>{{ task.title }} - {% if task.completed %}Done{% else %}Pending{% endif %}</li>
        {% endfor %}
    </ul>
</body>
</html>


******** Step 11: CRUD

1. Read (Already Done!)

2. Create (Add New Task)
To allow users to create tasks, we'll need:

A form for adding a new task.
A view to handle the form submission.
An entry in urls.py for the create task view.

a. Create Form
Create a file forms.py in your tasks app and add the following:

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']


b. Create View
In your views.py, create a view to handle creating new tasks:

from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks_list')  # Redirect to the task list after saving
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


c. Create Template
Create a new template for the task form, task_form.html:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Task</title>
</head>
<body>
    <h1>Add Task</h1>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
    <a href="{% url 'tasks_list' %}">Back to Task List</a>
</body>
</html>

d. In the task_list.html add a button to create new Tasks
<a href="{% url 'create_task' %}">
    <button>Create New Task</button>
</a>

3. Update (Edit Task)

A view to display the form with the task data pre-filled.
A template to handle editing (we can reuse the task_form.html).

a. Update View

def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=True)
        if form.is_valid():
            form.save()
            return redirect('tasks_list')
    else:
        form = TaskForm(instance=task)
    return render(request,'tasks/task_form.html',{'form':form})

b. Update urls.py

path('edit/<int:task_id>/', edit_task, name='edit_task'),


4. Delete (Remove Task)

A view to handle the deletion.
A button in the task list for deleting tasks.

a. Delete View


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks_list')
    return render(request, 'tasks/confirm_delete.html', {'task': task})


b. Delete Template

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete Task</title>
</head>
<body>
    <h1>Are you sure you want to delete "{{ task.title }}"?</h1>
    <form method="POST">
        {% csrf_token %}
        <button type="submit">Yes, Delete</button>
    </form>
    <a href="{% url 'tasks_list' %}">Cancel</a>
</body>
</html>


c. Update urls.py

path('delete/<int:task_id>/', delete_task, name='delete_task'),

d. Add Delete Button to Task List
In the task_list.html, add a delete link for each task:
<li>
    {{ task.title }} -
    {% if task.completed %}Done{% else %}Pending{% endif %}
    <a href="{% url 'edit_task' task.id %}">Edit</a> |
    <a href="{% url 'delete_task' task.id %}">Delete</a>
</li>
