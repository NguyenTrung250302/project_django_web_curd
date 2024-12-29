from django.urls import path
from . import views

urlpatterns = [
    # -------------------------------------------------------------------
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    #  -------------------------------------------------------------------
    path('home/', views.home_view, name='home'),
    # ---------------------------------------------------------------------
    # quản lý chương trình văn nghệ
    path('event_programs/', views.event_programs_view, name='event_programs'),
    path('event_programs/create/', views.create_event_view, name='create_event'),
    path('event_programs/<int:event_id>/edit/', views.edit_event_view, name='edit_event'),
    path('event_programs/<int:event_id>/delete/', views.delete_event_view, name='delete_event'),
    
    # quản lý các tiết mục mỗi chương trình
    path('tasks/', views.task_list_view, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
]
