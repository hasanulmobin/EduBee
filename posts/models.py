from django.db import models
from accounts.models import User, Student, Teacher


class TuitionPost(models.Model):
    MODE_CHOICES = [('online', 'Online'), ('offline', 'Offline'), ('both', 'Both')]
    STATUS_CHOICES = [('open', 'Open'), ('closed', 'Closed'), ('hired', 'Hired')]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tuition_posts')
    s_class = models.CharField(max_length=50)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    date = models.DateField()
    gender = models.CharField(max_length=10)
    time_slot = models.CharField(max_length=50)
    address = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    subject = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Post by {self.student.user.username} — {self.subject}"


class TuitionApplication(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='applications')
    tuition_post = models.ForeignKey(TuitionPost, on_delete=models.CASCADE, related_name='applications')
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('teacher', 'tuition_post')

    def __str__(self):
        return f"{self.teacher.user.username} → {self.tuition_post}"


class Payment(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')]
    METHOD_CHOICES = [('bkash', 'bKash'), ('nagad', 'Nagad'), ('bank', 'Bank'), ('cash', 'Cash')]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    tuition_post = models.ForeignKey(TuitionPost, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    paid_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Payment ৳{self.amount} — {self.status}"

