import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

url_currency = 'https://www.cbr.ru/currency_base/daily/'


def get_weather_new(city):

    url = 'http://api.weatherapi.com/v1/current.json'
    params = {'key': API_KEY, 'q': city}
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
    currency_data = {}
    for row in rows:
        cols = row.find_all('td')
        if cols:
            currency_code = cols[1].text.strip()
            if currency_code in ['USD', 'EUR', 'BYN']:
                currency_data[currency_code] = {
                    'Номинал': cols[2].text.strip(),
                    'Название': cols[3].text.strip(),
                    'Курс': cols[4].text.strip(),
                }

    output = ''
    order = ['USD', 'EUR', 'BYN']

    for code in order:
        if code in currency_data:
            info = currency_data[code]
            output += f"Валюта: {code}\n"
            output += f"Номинал: {info['Номинал']}\n"
            output += f"Название: {info['Название']}\n"
            output += f"Курс: {info['Курс']}\n"
            output += '-' * 15 + '\n'

    return output
