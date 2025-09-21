import requests
from bs4 import BeautifulSoup

url_weather = 'https://yandex.ru/pogoda/ru?lat=55.84537506&lon=37.3658371'
url_currency = 'https://www.cbr.ru/currency_base/daily/'

def get_weather():
    try:
        response = requests.get(url_weather)
        response.raise_for_status()
        html_response = response.text
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе: {e}')
        return 'Не удалось получить данные о погоде.'

    soup = BeautifulSoup(html_response, 'html.parser')
    degree = soup.find('p', class_='AppFactTemperature_content__Lx4p9')
    weather = soup.find('p', class_='AppFact_warning__8kUUn')
    feeling = soup.find('span', class_='AppFact_feels__IJoel AppFact_feels_withYesterday__yE440')

    if degree and weather and feeling:
        extracted_data = f"{degree.text} {weather.text} \n{feeling.text}"
        return extracted_data
    else:
        print('Один или несколько элементов парсинга не найдены')
        return 'Элемент не найден'

def get_currency():
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
        if cols and cols[1].text.strip() == 'USD':
            USD = f"Валюта: {cols[1].text.strip()} \nНоминал: {cols[2].text.strip()} \nНазвание: {cols[3].text.strip()} \nКурс: {cols[4].text.strip()}"
        if cols and cols[1].text.strip() == 'EUR':
            EUR = f"Валюта: {cols[1].text.strip()} \nНоминал: {cols[2].text.strip()} \nНазвание: {cols[3].text.strip()} \nКурс: {cols[4].text.strip()}"

    data = USD + '\n\n' + EUR
    return data
