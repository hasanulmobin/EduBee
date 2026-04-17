from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [

    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
path('student/', TemplateView.as_view(template_name='student.html'), name='student'),
path('review/', TemplateView.as_view(template_name='review.html'), name='review'),
]