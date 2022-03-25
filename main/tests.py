import datetime

from django.contrib.auth.models import User
from django.urls import reverse

from .models import Vacancy
from django.test import TestCase


class VacancyListTestCase(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='test_user', password='12345')
        test_user.save()
        vacancy_name = 'name'
        city = 'city'
        for i in range(1, 101):
            Vacancy.objects.create(
                user=test_user,
                vacancy_name=vacancy_name + str(i),
                city=city + str(i),
                min_salary=0,
                max_salary=100,
                currency='RUR',
                date_published = datetime.datetime.strptime('2022-02-25 15:00', '%Y-%m-%d %H:%M'),
                url='localhost:8000',
            )

    def test_vacancy_list(self):
        login = self.client.login(username='test_user', password='12345')
        server_response = self.client.get(reverse('main:result'))
        self.assertEqual(server_response.status_code, 200)
        self.assertTemplateUsed('main/result.html')
        self.assertTrue(server_response.context['form'], True)

    def test_vacancy_paginate(self):
        login = self.client.login(username='test_user', password='12345')
        server_response = self.client.get(reverse('main:result'))
        self.assertTrue(server_response.context['is_paginated'] == True)
        self.assertEqual(len(server_response.context['result']), 10)
        self.assertEqual(len(server_response.context['page_obj']), 10)

    # main

    def test_main(self):
        server_response = self.client.get(reverse('main:main'))
        self.assertEqual(server_response.status_code, 200)
        self.assertTemplateUsed('main/main.html')

    # delete

    def test_delete_view(self):
        self.client.login(username='test_user', password='12345')
        instances = Vacancy.objects.all()
        server_response = self.client.post(
            reverse('main:delete')
        )
        self.assertRedirects(
            server_response,
            reverse('main:result'),
            status_code=302
        )