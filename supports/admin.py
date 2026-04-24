from django.contrib import admin
from .models import Review, Message, Report, Notification


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['student', 'teacher', 'rating', 'date']
    list_filter   = ['rating']
    search_fields = ['student_userusername', 'teacheruser_username']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ['sender', 'receiver', 'time']
    search_fields = ['sender_username', 'receiver_username']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display  = ['reporter', 'reported', 'type', 'date']
    list_filter   = ['type']
    search_fields = ['reporter_username', 'reported_username']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ['recipient', 'sender', 'type', 'is_read', 'date']
    list_filter   = ['type', 'is_read']
    search_fields = ['recipient__username']