from http import HTTPStatus

from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse

from women.models import Women


class GetPagesTestCase(TestCase):
    fixtures = ['women_women.json', 'women_category.json', 'women_husband.json', 'women_tagpost.json']

    def setUp(self):
        "Инициализация перед выполнением каждого теста (каждого модуля)"
        pass

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Главная страница')
        self.assertTemplateUsed(response, 'women/index.html')

    def test_redirect_addpage(self):
        path = reverse('add_post')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertRedirects(response, redirect_uri)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_data_mainpage(self):
        w = Women.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], w[:5])

    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        w = Women.published.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['posts'], w[(page - 1) * paginate_by: page * paginate_by])


    def test_content_post(self):
        w = Women.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(response.context_data['post'].content, w.content)

    def tearDown(self):
        "Действия после выполнения каждого теста (каждого модуля)"
        pass
