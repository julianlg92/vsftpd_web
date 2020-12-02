from django.urls import path

from .views import user_update, delete_view, user_create, user_list

app_name = 'account'

urlpatterns = [
    path('create/', user_create, name='user_create'),
    path('users/', user_list, name='user_list'),
    path('<slug:pk>/edit/', user_update, name='update'),
    path('<slug:pk>/delete/', delete_view, name='delete'),
]
