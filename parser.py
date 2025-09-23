import requests
from bs4 import BeautifulSoup


url_currency = 'https://www.cbr.ru/currency_base/daily/'
api_key = 'a2d371551130439786c190020252309'

def get_weather_new(city):

    url = 'http://api.weatherapi.com/v1/current.json'
    params = {'key': api_key, 'q': city}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if 'error' in data:
            return "Error 0x0000001337"
        else:
            return f'Температура: {data['current']['temp_c']} \nСостояние погоды: {data['current']['condition']['text']} \nОщущается как: {data['current']['feelslike_c']} \nГород: {data['location']['name']}'
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def get_currency(cur):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url_currency, headers=headers)
        response.raise_for_status()
        html_response = response.text
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе: {e}')
        return 'Не удалось получить данные о курс валют'

    soup = BeautifulSoup(html_response, 'html.parser')

    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols and cols[1].text.strip() == cur:
            data = f"Валюта: {cols[1].text.strip()} \nНоминал: {cols[2].text.strip()} \nНазвание: {cols[3].text.strip()} \nКурс: {cols[4].text.strip()}"
            return data


def get_currency_all():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url_currency, headers=headers)
        response.raise_for_status()
        html_response = response.text
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе: {e}')
        return 'Не удалось получить данные о курс валют'

    soup = BeautifulSoup(html_response, 'html.parser')
    rows = soup.find_all('tr')
    data = ''
    for row in rows:
        cols = row.find_all('td')
        if cols and cols[1].text.strip() == 'USD':
            data += f"Валюта: {cols[1].text.strip()} \nНоминал: {cols[2].text.strip()} \nНазвание: {cols[3].text.strip()} \nКурс: {cols[4].text.strip()} \n"
            data += '-' * 15 + '\n'
    for row in rows:
        cols = row.find_all('td')
        if cols and cols[1].text.strip() == 'EUR':
            data += f"Валюта: {cols[1].text.strip()} \nНоминал: {cols[2].text.strip()} \nНазвание: {cols[3].text.strip()} \nКурс: {cols[4].text.strip()} \n"
            data += '-' * 15 + '\n'
    for row in rows:
        cols = row.find_all('td')
        if cols and cols[1].text.strip() == 'BYN':
            data += f"Валюта: {cols[1].text.strip()} \nНоминал: {cols[2].text.strip()} \nНазвание: {cols[3].text.strip()} \nКурс: {cols[4].text.strip()} \n"
    return data