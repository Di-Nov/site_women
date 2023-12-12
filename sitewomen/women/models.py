from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=WomenModel.Status.PUBLISHED)

class WomenModel(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='Слаг', blank=False, null=False)
    content = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', blank=True, default=None, null=True, verbose_name='Фото')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.IntegerField(choices=Status.choices, default=Status.PUBLISHED, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='cat_post', verbose_name='Категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags_post', verbose_name='Теги')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, blank=True, null=True, related_name='woman', verbose_name='Муж')

    objects = models.Manager()
    published = PublishedManager()


    class Meta:
        verbose_name = 'Женщины'
        verbose_name_plural = 'Женщины'
        ordering = ["-time_created"]
        indexes = [
            models.Index(fields=["-time_created"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     return super(self, WomenModel).save(*args, **kwargs)



class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, verbose_name='Слаг')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class TagPost(models.Model):
    tag = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)

    def __str__(self):
        return f"{self.tag} id:{self.id}"

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

