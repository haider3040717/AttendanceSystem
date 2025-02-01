from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('leave_request/', views.leave_request, name='leave_request'),
    path('attendance_report/', views.attendance_report, name='attendance_report'),
]