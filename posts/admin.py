from django.contrib import admin
from .models import TuitionPost, TuitionApplication, Payment


@admin.register(TuitionPost)
class TuitionPostAdmin(admin.ModelAdmin):
    list_display  = ['subject', 's_class', 'version', 'mode', 'salary', 'status', 'date']
    list_filter   = ['status', 'mode', 'gender']
    search_fields = ['subject', 's_class', 'student__user__username']


@admin.register(TuitionApplication)
class TuitionApplicationAdmin(admin.ModelAdmin):
    list_display  = ['teacher', 'tuition_post', 'status', 'date']
    list_filter   = ['status']
    search_fields = ['teacher__user__username']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ['student', 'teacher', 'tuition_post', 'amount', 'method', 'status', 'paid_date']
    list_filter   = ['status', 'method']
    search_fields = ['student_userusername', 'teacheruser_username']