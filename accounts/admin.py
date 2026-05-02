from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Teacher


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'join_date', 'is_active']
    list_filter = ['is_active', 'gender']
    search_fields = ['username', 'email', 'phone']

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {
            'fields': ('phone', 'address', 'gender', 'profile_picture')
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 's_class', 'version']
    search_fields = ['user__username', 's_class']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'verification_status', 'expected_salary']
    list_filter = ['verification_status']
    search_fields = ['user__username']

    actions = ['verify_teachers', 'reject_teachers']

    def verify_teachers(self, request, queryset):
        queryset.update(verification_status='verified')
    verify_teachers.short_description = "Mark selected teachers as Verified"

    def reject_teachers(self, request, queryset):
        queryset.update(verification_status='rejected')
    reject_teachers.short_description = "Mark selected teachers as Rejected"