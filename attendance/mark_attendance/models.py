from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from account.models import CustomUser
from django.utils.timezone import localdate
from datetime import timedelta, date

# Create your models here.

class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(default=now)
    status = models.CharField(max_length=10, choices=[("Present", "Present"), ("Absent", "Absent")])
    
    class Meta:
        unique_together = ('user', 'date')  # Prevent duplicate attendance for the same day.
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"

    # def save(self, *args, **kwargs):
    #     # Check if the same user already has an attendance record for the same day
    #     if Attendance.objects.filter(user=self.user, date=self.date).exists():
    #         raise ValidationError("You cannot mark attendance twice in a day.")
    #     super().save(*args, **kwargs)

    @staticmethod
    def mark_absent_for_previous_day():
        """
        Marks all unmarked attendance as 'Absent' for the previous day.
        """
        yesterday = date.today() - timedelta(days=1)  # Get the previous day
        users = CustomUser.objects.all()  # Get all users
        
        for user in users:
            # Check if the user already has an attendance record for yesterday
            if not Attendance.objects.filter(user=user, date=yesterday).exists():
                # If no attendance exists, mark it as "Absent"
                Attendance.objects.create(user=user, date=yesterday, status="Absent")

    def save(self, *args, **kwargs):
        # Ensure no duplicate attendance records for the same day
        if Attendance.objects.filter(user=self.user, date=self.date).exists():
            raise ValidationError("You cannot mark attendance twice in a day.")
        super().save(*args, **kwargs)



class LeaveRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="leave_requests")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )
    request_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date} - {self.status}"




class AttendanceReport(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reports")
    from_date = models.DateField()
    to_date = models.DateField()
    present_days = models.PositiveIntegerField(default=0)
    absent_days = models.PositiveIntegerField(default=0)
    leave_days = models.PositiveIntegerField(default=0)
    grade = models.CharField(max_length=2, blank=True, null=True)  # Grade assigned based on attendance

    def calculate_grade(self):
        """
        Automatically calculates and assigns a grade based on the number of present days.
        """

        if self.to_date and self.from_date:
            # Calculate the total days in the given range
            total_days = (self.to_date - self.from_date).days + 1  # +1 to include the last day

            # Avoid division by zero in case of invalid date range
            if total_days > 0:
                ratio = self.present_days / total_days

                # Assign grade based on the ratio
                if 0.8 <= ratio <= 1.0:
                    return "A"
                elif 0.6 <= ratio < 0.8:
                    return "B"
                elif 0.4 <= ratio < 0.6:
                    return "C"
                else:
                    return "D"
            else:
                return "D"  # Default grade for invalid date ranges
        else:
            return "D"  # Default grade if dates are not provided

    def save(self, *args, **kwargs):
        # Calculate the grade before saving
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Report for {self.user.username}: {self.from_date} to {self.to_date} - Grade {self.grade}"
