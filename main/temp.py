import requests

url = f'https://api.hh.ru/vacancies/?text=django&per_page=30'
resp = requests.get(url)
dict = resp.json()
result = []
result.append(dict)
# for num in range(1, dict['pages']):
#     if (dict['pages'] - num) <= 1:
#         break
#     response = requests.get(url=url + f'&page={num}')
#     result.append(response.json())
for i in dict['items']:
    print(i['alternate_url'])
# print(result)


