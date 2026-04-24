from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from posts.models import TuitionPost
from accounts.models import Teacher, Student


def home(request):
    context = {
        'total_posts':    TuitionPost.objects.filter(status='open').count(),
        'total_teachers': Teacher.objects.filter(verification_status='verified').count(),
        'total_students': Student.objects.all().count(),
        'recent_posts':   TuitionPost.objects.filter(status='open').order_by('-date')[:6],
    }
    return render(request, 'home.html', context)


urlpatterns = [
    path('admin/',    admin.site.urls),
    path('',          home,                     name='home'),
    path('accounts/', include('accounts.urls')),
    path('posts/',    include('posts.urls')),
    path('supports/', include('supports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)