from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name="index"),
    path('create_todo/', views.create_todo, name='create_todo'),
    path('get_todos/', views.get_todos, name='get_todos'),
]