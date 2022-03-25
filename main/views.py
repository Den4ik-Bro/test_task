from celery.result import AsyncResult
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from .models import *
from .forms import SearchForm
from .tasks import hh_vacancy


class Main(generic.TemplateView):
    template_name = 'main/main.html'

    def get(self, request, *args, **kwargs):
        return super().get(request)


class GetVacancy(generic.FormView):
    template_name = 'main/get_vacancy.html'
    model = Vacancy
    form_class = SearchForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = hh_vacancy.delay(form.cleaned_data['text'])
            result = task.get()
            vacancy_list = []
            for page in result:
                for item in page['items']:
                    if item['salary']:
                        vacancy = Vacancy(
                            user=request.user,
                            vacancy_name=item['name'],
                            city=item['area']['name'],
                            min_salary=item['salary'].get('from', 0),
                            max_salary=item['salary'].get('to', 0),
                            currency=item['salary']['currency'],
                            date_published=item['published_at'],
                            url=item['alternate_url'],
                        )
                        vacancy_list.append(vacancy)
                    else:
                        vacancy = Vacancy(
                            user=request.user,
                            vacancy_name=item['name'],
                            city=item['area']['name'],
                            date_published=item['published_at'],
                            url = item['alternate_url'],
                        )
                        vacancy_list.append(vacancy)
            Vacancy.objects.bulk_create(vacancy_list)
            return redirect(reverse('main:result'))
        return redirect(reverse('main:result'))


class Result(generic.ListView):
    queryset = Vacancy.objects.all()
    template_name = 'main/result.html'
    context_object_name = 'result'
    paginate_by = 10
    form_class = SearchForm

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        if 'text' in self.request.GET:
            form = self.form_class(self.request.GET)
            if form.is_valid():
                queryset = queryset.filter(
                    Q(vacancy_name=form.cleaned_data['text']) |
                    Q(city=form.cleaned_data['text'])
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class()
        context['form'] = form
        context['text'] = self.request.GET.get('text')
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        paginator, page, queryset, is_paginated = self.paginate_queryset \
                (
                self.object_list,
                self.paginate_by
            )
        context.update({
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
            self.context_object_name: queryset
        })
        return self.render_to_response(context)


class DeleteResult(generic.RedirectView):

    def post(self, request, *args, **kwargs):
        queryset = Vacancy.objects.filter(user=self.request.user)
        queryset.delete()
        return redirect(reverse('main:result'))