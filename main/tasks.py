from celery import shared_task
import requests


@shared_task()
def hh_vacancy(text):
    url = f'https://api.hh.ru/vacancies/?text={text}&per_page=100'
    resp = requests.get(url)
    dict = resp.json()
    result = []
    for num in range(1, dict['pages']):
        if (dict['pages'] - num) <= 1:
            break
        response = requests.get(url=url + f'&page={num}')
        result.append(response.json())
    return result


