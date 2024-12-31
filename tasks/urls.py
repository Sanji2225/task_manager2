from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks', views.listarTasks, name='tasks'),
    path('nova_task', views.novaTask, name='novaTask'),

    path('tasks/<task_id>/', views.task, name='task'),
    path('edit_task/<task_id>/', views.editTask, name='edit_task'),

    path('delete_task/<task_id>/', views.deleteTask, name='delete_task'),

    path('confirmdelete_task/<task_id>/', views.confirmDeleteTask, name='confirmDelete_task'),
    path('naoexiste', views.erro404, name='Erro404'),
]
