from django.urls import path
from . import views

urlpatterns = [

    path('register/',                         views.register,          name='register'),
    path('login/',                            views.user_login,        name='user_login'),
    path('logout/',                           views.user_logout,       name='user_logout'),
    path('dashboard/',                        views.dashboard,         name='dashboard'),
    path('profile/update/',                   views.update_profile,    name='update_profile'),


    path('teachers/',                         views.teacher_list,      name='teacher_list'),
    path('teachers/<int:pk>/',                views.teacher_detail,    name='teacher_detail'),


    path('admin/teachers/',                   views.all_teachers,      name='all_teachers'),
    path('admin/teachers/verify/<int:pk>/',   views.verify_teacher,    name='verify_teacher'),
    path('admin/users/',                      views.all_users,         name='all_users'),
    path('admin/users/delete/<int:pk>/',      views.delete_user,       name='delete_user'),
    path('admin/users/toggle/<int:pk>/',      views.toggle_user_active,name='toggle_user_active'),
]