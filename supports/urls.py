from django.urls import path
from . import views

urlpatterns = [
    # Reviews
    path('review/teacher/<int:teacher_pk>/',  views.review_create,  name='review_create'),
    path('review/<int:pk>/update/',           views.review_update,  name='review_update'),
    path('review/<int:pk>/delete/',           views.review_delete,  name='review_delete'),
    # Messages
    path('inbox/',                            views.inbox,          name='inbox'),
    path('message/send/<int:receiver_pk>/',   views.send_message,   name='send_message'),
    path('message/<int:pk>/delete/',          views.message_delete, name='message_delete'),
    # Report
    path('report/<int:user_pk>/',             views.report_user,    name='report_user'),
    # Notifications
    path('notifications/',                    views.notification_list, name='notification_list'),
]