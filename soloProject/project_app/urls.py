from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('home', views.success),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('createtask', views.create),
    path('<int:task_id>/delete', views.delete_task),
    path('task/<int:task_id>', views.task),
    path('task/<int:task_id>/assign', views.assign_task),
    path('task/assign/<int:task_id>', views.taskAssignment),
    path('drop/<int:task_id>', views.drop_task),
    path('user/<int:user_id>', views.user_profile),
    path('user/edit/<int:user_id>', views.edit_profile),
    path('user/<int:user_id>/edit', views.update_profile),
    path('task/update/<int:task_id>', views.edit_task),
    path('task/<int:task_id>/update', views.update_task),
    path('task/<int:task_id>/complete', views.complete_task),
    path('completed', views.completed)
]
