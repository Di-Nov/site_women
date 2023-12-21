from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        '''
        Класс AuthenticationForm работатет с моделью User, тут мы их явно привяжем.
        При такой привязке, можно обойтись без атрибутов, но лучше прописать widget для password
        '''

        model = get_user_model()  # Получаем модель пользователя, через метод потому что она в будущем может измениться, и чтоб не получить ошибку пишем так.
        fields = ['username',
                  'password']  # отображаем поля 'username', 'password', но чтоб к нему прикрутились виждеты, переопределим атрибутами


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50, label='Логин')
    password = forms.CharField(max_length=50, label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'E-mail',
        }

    def clean_password2(self):  # Ручная валидация поля password2. Вернуть password2
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_email(self):  # Ручная валидация поля email. Вернуть email
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Такой E-mail уже существует')
        return email
