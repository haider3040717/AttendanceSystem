from django import forms
from .models import Attendance, LeaveRequest
from datetime import date

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[("Present", "Present"), ("Absent", "Absent")], attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Retrieve the logged-in user from kwargs
        super(AttendanceForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AttendanceForm, self).save(commit=False)
        instance.date = date.today()  # Automatically set the date when the attendance is marked
        if self.user:
            instance.user = self.user  # Assign the logged-in user
        if commit:
            instance.save()
        return instance




class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']  # Exclude `user` and `status`
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control', 
                'placeholder': 'Select start date'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control', 
                'placeholder': 'Select end date'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Enter the reason for leave'
            }),
        }




class AttendanceReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.SelectDateWidget())
    to_date = forms.DateField(widget=forms.SelectDateWidget())