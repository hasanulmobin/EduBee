from django.db import models
from accounts.models import User, Student, Teacher


class Review(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reviews')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='reviews')
    rating  = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    date    = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'teacher')

    def __str__(self):
        return f"Review by {self.student.user.username} → {self.teacher.user.username}"


class Message(models.Model):
    sender   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    time     = models.DateTimeField(auto_now_add=True)
    content  = models.TextField()

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"


class Report(models.Model):
    TYPE_CHOICES = [('spam', 'Spam'), ('abuse', 'Abuse'), ('fake', 'Fake Profile'), ('other', 'Other')]

    reporter    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')
    type        = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date        = models.DateField(auto_now_add=True)
    overview    = models.TextField()

    def __str__(self):
        return f"Report: {self.reporter.username} → {self.reported.username}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('application', 'Application'),
        ('payment',     'Payment'),
        ('message',     'Message'),
        ('review',      'Review'),
        ('system',      'System'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sender               = models.ForeignKey(User, on_delete=models.CASCADE,
                                             related_name='sent_notifications', null=True, blank=True)
    type                 = models.CharField(max_length=30, choices=TYPE_CHOICES)
    notification_details = models.TextField()
    date                 = models.DateField(auto_now_add=True)
    is_read              = models.BooleanField(default=False)

    def __str__(self):
        return f"Notif → {self.recipient.username}: {self.type}"