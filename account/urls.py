from django.urls import path

from .views import user_update, delete_view, user_create, user_list, user_enable, requests

app_name = 'account'

urlpatterns = [
    path('create/', user_create, name='user_create'),
    path('enabled_users_list/', user_list, {'exclude_enable': False}, name='enabled_user_list'),
    path('disabled_users_list/', user_list, {'exclude_enable': True}, name='disabled_user_list'),
    path('requests/', requests, name='requests'),
    path('<slug:pk>/edit/', user_update, name='update'),
    path('<slug:pk>/delete/', delete_view, name='delete'),
    path('<slug:pk>/enable/', user_enable, name='enable')
]
