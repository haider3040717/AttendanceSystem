from django.contrib import admin
from .models import Attendance, LeaveRequest, AttendanceReport

# Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'status',]

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'end_date', 'reason', 'status', 'request_date',]

class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'from_date', 'to_date', 'present_days', 'absent_days', 'leave_days', 'grade',]


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(LeaveRequest, LeaveRequestAdmin)
admin.site.register(AttendanceReport, AttendanceReportAdmin)