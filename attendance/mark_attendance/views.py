from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import AttendanceForm, LeaveRequestForm, AttendanceReportForm
from .models import Attendance, LeaveRequest, AttendanceReport
from django.contrib import messages

# Create your views here.

@login_required(login_url='user_login')
def home(request):
    return render(request, 'frontend/home.html', {})


# @login_required(login_url='user_login')
# def mark_attendance(request):
#     if request.method == 'POST':
#         form = AttendanceForm(request.POST)
#         if form.is_valid():
#             try:
#                 # Save the form and handle ValidationError from the model
#                 attendance = form.save(commit=False)
#                 attendance.user = request.user  # Set the logged-in user
#                 attendance.save()
#                 messages.success(request, "Attendance marked successfully!")
#             except ValidationError as e:
#                 # Add the error message to Django messages
#                 messages.error(request, str(e))
#             return redirect('mark_attendance')
#         else:
#             messages.error(request, "Invalid form submission. Please check the details.")
#     else:
#         form = AttendanceForm()
    
#     return render(request, 'frontend/mark_attendance.html', {'form': form})


@login_required(login_url='user_login')
def mark_attendance(request):
    # Ensure absentees are marked for the previous day
    Attendance.mark_absent_for_previous_day()

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            try:
                # Save the form and handle ValidationError from the model
                attendance = form.save(commit=False)
                attendance.user = request.user  # Set the logged-in user
                attendance.save()
                messages.success(request, "Attendance marked successfully!")
            except ValidationError as e:
                # Add the error message to Django messages
                messages.error(request, str(e))
            return redirect('mark_attendance')
        else:
            messages.error(request, "Invalid form submission. Please check the details.")
    else:
        form = AttendanceForm()
    
    return render(request, 'frontend/mark_attendance.html', {'form': form})



@login_required(login_url='user_login')
def leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user  # Automatically set the logged-in user
            leave_request.save()
            messages.success(request, 'Your leave request has been submitted.')
            return redirect('leave_request')  # Redirect to a relevant page
        else:
            messages.error(request, 'There was an error in your form.')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'frontend/leave_request.html', {'form': form})



@login_required(login_url='user_login')
def attendance_report(request):
    context = {}
    
    if request.method == "POST":
        form = AttendanceReportForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            
            # Get the logged-in user
            user = request.user
            
            # Query for attendance within the date range
            present_days = Attendance.objects.filter(
                user=user,
                date__gte=from_date,
                date__lte=to_date,
                status="Present"
            ).count()
            
            absent_days = Attendance.objects.filter(
                user=user,
                date__gte=from_date,
                date__lte=to_date,
                status="Absent"
            ).count()
            
            # Query for approved leave requests within the date range
            leave_days = LeaveRequest.objects.filter(
                user=user,
                start_date__lte=to_date,
                end_date__gte=from_date,
                status="Approved"
            ).count()

            # Create or update the attendance report
            attendance_report, created = AttendanceReport.objects.update_or_create(
                user=user,
                from_date=from_date,
                to_date=to_date,
                defaults={
                    'present_days': present_days,
                    'absent_days': absent_days,
                    'leave_days': leave_days,
                    'grade': None  # We'll calculate the grade afterward
                }
            )
            
            # Calculate the grade
            grade = attendance_report.calculate_grade()
            attendance_report.grade = grade
            attendance_report.save()

            context.update({
                'form': form,
                'from_date': from_date,
                'to_date': to_date,
                'present_days': present_days,
                'absent_days': absent_days,
                'leave_days': leave_days,
                'grade': grade
            })
        else:
            context['form'] = form
    else:
        form = AttendanceReportForm()
        context['form'] = form
    
    return render(request, 'frontend/attendance_report.html', context)