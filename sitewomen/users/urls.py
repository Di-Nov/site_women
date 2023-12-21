from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views


app_name = 'users' # Записывается при указании spacename в urls.py

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.refister_user, name='register'),
]


