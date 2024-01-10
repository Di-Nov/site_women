from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from django.urls import path

from users import views


app_name = 'users' # Записывается при указании spacename в urls.py

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('password_change/', views.ProfilePasswordChangeView.as_view(), name='password_change'),
    path('change_password/done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'), name='password_change_done'),
]


