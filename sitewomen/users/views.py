from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    '''
    Перенаправление при успешной авторизации прописывается в настройках - LOGIN_REDIRECT_URL = 'home'
    '''

    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     ''' Имеет больший приоритет чем параметр next в forms.py, поэтому лучше использовать LOGIN_REDIRECT_URL = 'home'
    #      в связке с параметром next в forms.py (сормируется самостоятельно и передается в шаблон)'''
    #     return reverse_lazy('home')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': "Регистрация"}


class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя",
                     'default_image': settings.DEFAULT_USER_IMAGE
                     }
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class ProfilePasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Изменение пароля'}


# def register_user(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # создание объекта без сохранения в БД
#             user.set_password(request.POST['password'])
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})

# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#
#     else:
#         form = LoginUserForm()
#         return render(request, 'users/login.html', context={'form': form})

# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))
