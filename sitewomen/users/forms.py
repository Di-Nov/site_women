from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        '''
        Класс AuthenticationForm работатет с моделью User, тут мы их явно привяжем.
        При такой привязке, можно обойтись без атрибутов
        '''

        model = get_user_model() # Получаем модель пользователя, через метод потому что она в будущем может измениться, и чтоб не получить ошибку пишем так.
        fields = ['username', 'password'] # отображаем поля 'username', 'password', но чтоб к нему прикрутились виждеты, переопределим атрибутами
