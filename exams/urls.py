from django.urls import path
from . import views

urlpatterns = [
    path('take/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('submit/<int:exam_id>/', views.submit_exam, name='submit_exam'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='exams_home'),
]
