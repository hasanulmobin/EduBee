from django.contrib import admin
from .models import Review, Message, Report, Notification


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['student', 'teacher', 'rating', 'date']
    list_filter   = ['rating']
    search_fields = ['student_userusername', 'teacheruser_username']