from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, WomenModel


@deconstructible
class RussianValidator:
    '''Создание своего валидатора. Применяется при условии, что испрользуется часто,
    если нужен частный случай, используется метод clean_**(self): для каждого поля в своей форме'''

    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем",
                                     label="Муж")

    class Meta:
        model = WomenModel
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
        # labels = {}

    def clean_title(self):
        '''Валидация поля title вручную'''
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл', required=True)


# Пример построение форм без привязки к моделям.
# Это не лучшая практика если есть модель которую можно привязать к форме
"""
class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5, label="Заголовок",
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={
                                'min_length': 'Слишком короткий заголовок',
                                'max_length': 'Без заголовка - никак'
                            },
                            validators=[RussianValidator()])
    slug = forms.SlugField(max_length=255, label="Слаг",
                           validators=[
                               MaxLengthValidator(255, message='Максимум 100 символов'),
                               MinLengthValidator(5, 'Минимум 5 символов')])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана",
                                 label="Категории")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False,
                                     empty_label="Не замужем", label="Муж")

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны быть только русские символы, дефис и пробел.")
        return title
"""


