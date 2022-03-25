from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('get_vacancy/', views.GetVacancy.as_view(), name='get_vacancy'),
    path('result/', views.Result.as_view(), name='result'),
    path('delete_result/', views.DeleteResult.as_view(), name='delete'),
]