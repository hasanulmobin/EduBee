from django.urls import path
from . import views

urlpatterns = [
    path('register/',          views.register,       name='register'),
    path('login/',             views.user_login,      name='user_login'),
    path('logout/',            views.user_logout,     name='user_logout'),
    path('dashboard/',         views.dashboard,       name='dashboard'),
    path('profile/update/',    views.update_profile,  name='update_profile'),
    path('teachers/',          views.teacher_list,    name='teacher_list'),
    path('teachers/<int:pk>/', views.teacher_detail,  name='teacher_detail'),
]