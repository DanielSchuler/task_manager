from django.urls import path
from .views import task_list, create_task, edit_task,delete_task

urlpatterns = [
    path('', task_list, name='tasks_list'),
    path('create/', create_task, name='create_task'),
    path('edit/<int:task_id>/', edit_task, name='edit_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),

]
