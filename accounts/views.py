from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden

from .models import User, Student, Teacher
from .forms import RegisterForm, StudentProfileForm, TeacherProfileForm, UserUpdateForm



def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user_login')
        if not request.user.is_superuser:
            return HttpResponseForbidden(
                " Access Denied. Only admin can access this page."
            )
        return view_func(request, *args, **kwargs)
    return wrapper



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user      = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            if user.role == 'student':
                Student.objects.get_or_create(user=user)
            elif user.role == 'teacher':
                Teacher.objects.get_or_create(user=user)
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

    if request.user.is_superuser:

        context['total_teachers']         = Teacher.objects.count()
        context['pending_teachers']       = Teacher.objects.filter(verification_status='pending').count()
        context['verified_teachers']      = Teacher.objects.filter(verification_status='verified').count()
        context['rejected_teachers']      = Teacher.objects.filter(verification_status='rejected').count()
        context['total_students']         = Student.objects.count()
        context['total_users']            = User.objects.count()
        return render(request, 'accounts/admin_dashboard.html', context)

    elif request.user.role == 'student':
        profile, _ = Student.objects.get_or_create(user=request.user)
        context['profile'] = profile

    elif request.user.role == 'teacher':
        profile, _ = Teacher.objects.get_or_create(user=request.user)
        context['profile'] = profile

    return render(request, 'accounts/dashboard.html', context)



@login_required
def update_profile(request):
    user = request.user

    if user.role == 'student':
        profile, _       = Student.objects.get_or_create(user=user)
        ProfileFormClass = StudentProfileForm
    elif user.role == 'teacher':
        profile, _       = Teacher.objects.get_or_create(user=user)
        ProfileFormClass = TeacherProfileForm
    else:
        profile          = None
        ProfileFormClass = None

    if request.method == 'POST':
        user_form    = UserUpdateForm(request.POST, request.FILES, instance=user)
        profile_form = ProfileFormClass(request.POST, instance=profile) if ProfileFormClass else None

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            return redirect('dashboard')
    else:
        user_form    = UserUpdateForm(instance=user)
        profile_form = ProfileFormClass(instance=profile) if ProfileFormClass else None

    return render(request, 'accounts/update_profile.html', {
        'user_form':    user_form,
        'profile_form': profile_form,
    })


def teacher_list(request):
    teachers = Teacher.objects.select_related('user').filter(
        verification_status='verified'
    )
    return render(request, 'accounts/teacher_list.html', {'teachers': teachers})



def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'accounts/teacher_detail.html', {'teacher': teacher})



@admin_required
def all_teachers(request):
    teachers = Teacher.objects.select_related('user').all().order_by('verification_status')
    return render(request, 'accounts/all_teachers.html', {'teachers': teachers})


@admin_required
def verify_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'verify':
            teacher.verification_status = 'verified'
            teacher.save()
            try:
                from supports.notifications import notify_teacher_verified
                notify_teacher_verified(teacher.user)
            except Exception as e:
                print(f"Notification error: {e}")

        elif action == 'reject':
            teacher.verification_status = 'rejected'
            teacher.save()
            try:
                from supports.notifications import notify_teacher_rejected
                notify_teacher_rejected(teacher.user)
            except Exception as e:
                print(f"Notification error: {e}")

        elif action == 'pending':
            teacher.verification_status = 'pending'
            teacher.save()

    return redirect('all_teachers')


@admin_required
def all_users(request):
    users = User.objects.all().order_by('role', 'username')
    return render(request, 'accounts/all_users.html', {'users': users})



@admin_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
    return redirect('all_users')



@admin_required
def toggle_user_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
    return redirect('all_users')