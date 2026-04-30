from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin',   'Admin'),
    ]
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    role            = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    phone           = models.CharField(max_length=20, blank=True)
    address         = models.TextField(blank=True)
    gender          = models.CharField(max_length=10, blank=True)
    join_date       = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    def __str__(self):
        return f"{self.username} ({self.role})"


class Student(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    s_class    = models.CharField(max_length=50)
    version    = models.CharField(max_length=50)
    background = models.TextField(blank=True)

    def __str__(self):
        return f"Student: {self.user.username}"


class Teacher(models.Model):
    VERIFICATION_CHOICES = [
        ('pending',  'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    user                = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio                 = models.TextField(blank=True)
    verification_status = models.CharField(
                              max_length=20,
                              choices=VERIFICATION_CHOICES,
                              default='pending'
                          )
    expected_salary     = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Teacher: {self.user.username}"