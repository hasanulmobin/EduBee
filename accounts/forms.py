from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Teacher

def add_bootstrap(form):
    for field in form.fields.values():
        widget = field.widget
        if hasattr(widget, 'attrs'):
            existing = widget.attrs.get('class', '')
            if 'form-control' not in existing and 'form-select' not in existing:
                from django.forms import Select, CheckboxInput
                if isinstance(widget, Select):
                    widget.attrs['class'] = existing + ' form-select'
                elif isinstance(widget, CheckboxInput):
                    widget.attrs['class'] = existing + ' form-check-input'
                else:
                    widget.attrs['class'] = existing + ' form-control'
class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [('student', 'Student'), ('teacher', 'Teacher')]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'phone', 'address', 'gender', 'profile_picture',
                  'password1', 'password2', 'role']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = ['s_class', 'version', 'background']
        widgets = {
            'background': forms.Textarea(attrs={'rows': 3}),
        }


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model  = Teacher
        fields = ['bio', 'expected_salary']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email',
                  'phone', 'address', 'gender', 'profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }