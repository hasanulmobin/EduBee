from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review, Message, Report, Notification
from .forms import ReviewForm, MessageForm, ReportForm
from accounts.models import User, Student, Teacher


# ---------- Review CRUD ----------

@login_required
def review_create(request, teacher_pk):
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review         = form.save(commit=False)
            review.student = student
            review.teacher = teacher
            review.save()
            # Auto-create notification for teacher
            Notification.objects.create(
                recipient=teacher.user,
                sender=request.user,
                type='review',
                notification_details=f"{request.user.username} left you a review."
            )
            return redirect('teacher_detail', pk=teacher_pk)
    else:
        form = ReviewForm()
    return render(request, 'supports/review_form.html', {'form': form, 'teacher': teacher})


@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('teacher_detail', pk=review.teacher.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'supports/review_form.html', {'form': form})


@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    teacher_pk = review.teacher.pk
    if request.method == 'POST':
        review.delete()
    return redirect('teacher_detail', pk=teacher_pk)


# ---------- Message CRUD ----------

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-time')
    return render(request, 'supports/inbox.html', {'messages': messages})


@login_required
def send_message(request, receiver_pk):
    receiver = get_object_or_404(User, pk=receiver_pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg          = form.save(commit=False)
            msg.sender   = request.user
            msg.receiver = receiver
            msg.save()
            Notification.objects.create(
                recipient=receiver,
                sender=request.user,
                type='message',
                notification_details=f"New message from {request.user.username}."
            )
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'supports/message_form.html', {'form': form, 'receiver': receiver})


@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
    return redirect('inbox')


# ---------- Report ----------

@login_required
def report_user(request, user_pk):
    reported_user = get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report          = form.save(commit=False)
            report.reporter = request.user
            report.reported = reported_user
            report.save()
            return redirect('dashboard')
    else:
        form = ReportForm()
    return render(request, 'supports/report_form.html', {'form': form, 'reported': reported_user})


# ---------- Notification ----------

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(
        recipient=request.user).order_by('-date')
    notifications.filter(is_read=False).update(is_read=True)   # mark all as read
    return render(request, 'supports/notifications.html', {'notifications': notifications})