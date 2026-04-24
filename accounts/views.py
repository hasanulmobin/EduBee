from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Student, Teacher
from .forms import RegisterForm, StudentProfileForm, TeacherProfileForm, UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user      = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            # Auto-create role-specific profile
            if user.role == 'student':
                Student.objects.create(user=user)
            elif user.role == 'teacher':
                Teacher.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def dashboard(request):
    context = {'user': request.user}
    if request.user.role == 'student':
        context['profile'] = get_object_or_404(Student, user=request.user)
    elif request.user.role == 'teacher':
        context['profile'] = get_object_or_404(Teacher, user=request.user)
    return render(request, 'accounts/dashboard.html', context)


@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if user.role == 'student':
            profile_form = StudentProfileForm(request.POST, instance=user.student)
        else:
            profile_form = TeacherProfileForm(request.POST, instance=user.teacher)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = StudentProfileForm(instance=user.student) if user.role == 'student' \
                       else TeacherProfileForm(instance=user.teacher)

    return render(request, 'accounts/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


# Teacher list (public)
def teacher_list(request):
    teachers = Teacher.objects.select_related('user').filter(verification_status='verified')
    return render(request, 'accounts/teacher_list.html', {'teachers': teachers})


def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'accounts/teacher_detail.html', {'teacher': teacher})