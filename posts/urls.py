from django.urls import path
from . import views

urlpatterns = [
    # TuitionPost
    path('',                              views.post_list,                 name='post_list'),
    path('<int:pk>/',                     views.post_detail,               name='post_detail'),
    path('create/',                       views.post_create,               name='post_create'),
    path('<int:pk>/update/',              views.post_update,               name='post_update'),
    path('<int:pk>/delete/',              views.post_delete,               name='post_delete'),
    # Applications
    path('<int:post_pk>/apply/',          views.apply_post,                name='apply_post'),
    path('application/<int:pk>/withdraw/', views.withdraw_application,     name='withdraw_application'),
    path('application/<int:pk>/status/',   views.update_application_status,name='update_application_status'),
    # Payment
    path('<int:post_pk>/pay/',            views.payment_create,            name='payment_create'),
    path('payments/',                     views.payment_list,              name='payment_list'),
       path('<int:pk>/close/',              views.close_post,        name='close_post'),
    path('<int:post_pk>/hire/<int:application_pk>/', views.hire_teacher, name='hire_teacher'),
    path('teacher/payments/', views.teacher_payments, name='teacher_payments'),
    path('my-posts/', views.my_posts, name='my_posts'),
]