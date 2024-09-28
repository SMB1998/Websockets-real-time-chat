# En tu_app/urls.py
from django.urls import path
from .views import create_user, read_user,update_password, update_user, delete_user, login_view, password_reset_request,password_reset_confirm
urlpatterns = [
    path('user/', create_user, name='create_user'), 
    path('users/<int:user_id>/', read_user, name='read_user'),
    path('user-update/<int:user_id>/', update_user, name='update_user'),
    path('user-delete/<int:user_id>/', delete_user, name='delete_user'),
    path('user-update-password/<int:user_id>/', update_password, name='update_password'),
    path('login/', login_view, name='login'),
    path('password_reset/', password_reset_request, name='password_reset_request'),
     path('reset_password_confirm/<int:id>/<token>/<password>/', password_reset_confirm, name='password_reset_confirm'),
]
