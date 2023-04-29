
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.get_all_students_id, name='all-student'),
    path('create/', views.create_student_id, name='create-id-card'),
    path('<uuid:student_id>/', views.get_student_id, name='get-student-id'),
    path('edit/<uuid:id>/', views.edit_student_id, name='edit-student-id'),
    path('delete/<uuid:id>/', views.delete_student_id, name='delete-student-id'),
]

