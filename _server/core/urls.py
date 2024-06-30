from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name="index"),
    path('create_todo/', views.create_todo, name='create_todo'),
    path('get_todos/', views.get_todos, name='get_todos'),
    path('update_todo/<int:todo_id>/', views.update_todo, name='update_todo'),
    path('get_todo/<int:todo_id>/', views.get_todo, name='get_todo'),
    path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('hello_world/', views.hello_world, name='hello_world'),
]