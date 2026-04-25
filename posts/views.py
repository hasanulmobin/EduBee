from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TuitionPost, TuitionApplication, Payment
from .forms import TuitionPostForm, TuitionApplicationForm, PaymentForm
from accounts.models import Student, Teacher




def post_list(request):
    posts = TuitionPost.objects.filter(status='open').order_by('-date')
    return render(request, 'posts/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(TuitionPost, pk=pk)
    applications = post.applications.select_related('teacher__user').all()
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'applications': applications
    })


@login_required
def post_create(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        form = TuitionPostForm(request.POST)
        if form.is_valid():
            post         = form.save(commit=False)
            post.student = student
            post.save()
            return redirect('post_list')
    else:
        form = TuitionPostForm()
    return render(request, 'posts/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_update(request, pk):
    post = get_object_or_404(TuitionPost, pk=pk)
    if request.method == 'POST':
        form = TuitionPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = TuitionPostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form, 'action': 'Update'})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(TuitionPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})




@login_required
def apply_post(request, post_pk):
    post    = get_object_or_404(TuitionPost, pk=post_pk)
    teacher = get_object_or_404(Teacher, user=request.user)
    TuitionApplication.objects.get_or_create(teacher=teacher, tuition_post=post)
    return redirect('post_detail', pk=post_pk)


@login_required
def withdraw_application(request, pk):
    application = get_object_or_404(TuitionApplication, pk=pk)
    post_pk     = application.tuition_post.pk
    if request.method == 'POST':
        application.delete()
    return redirect('post_detail', pk=post_pk)


@login_required
def update_application_status(request, pk):
    application = get_object_or_404(TuitionApplication, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['accepted', 'rejected']:
            application.status = status
            application.save()
    return redirect('post_detail', pk=application.tuition_post.pk)




@login_required
def payment_create(request, post_pk):
    post    = get_object_or_404(TuitionPost, pk=post_pk)
    student = get_object_or_404(Student, user=request.user)
    accepted_app = post.applications.filter(status='accepted').first()
    if not accepted_app:
        return redirect('post_detail', pk=post_pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment              = form.save(commit=False)
            payment.student      = student
            payment.teacher      = accepted_app.teacher
            payment.tuition_post = post
            payment.save()
            return redirect('dashboard')
    else:
        form = PaymentForm()
    return render(request, 'posts/payment_form.html', {'form': form, 'post': post})


@login_required
def payment_list(request):
    student  = get_object_or_404(Student, user=request.user)
    payments = Payment.objects.filter(student=student).order_by('-paid_date')
    return render(request, 'posts/payment_list.html', {'payments': payments})