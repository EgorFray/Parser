import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://auto.ria.com/newauto/marka-jeep/'
HEADERS ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
          'Accept': '*/*'
          }
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Цена USD', 'Цена UA', 'Город', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['price_usd'], item['price_ua'], item['city'], item['link']])




def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')

    cars =[]

    for item in items:
        uah_price = item.find('span', class_='grey size13')
        if uah_price:
            uah_price = uah_price.get_text(strip=True)
        else:
            uah_price = 'Not Defined'

        cars.append({
            'title': item.find('div', class_='proposition_title').get_text(strip=True),
            'price_usd': item.find('span', class_='green').get_text(strip=True),
            'price_ua': uah_price,
            'city': item.find('svg', class_='svg-i16_pin').find_next('strong').get_text(),
            'link': HOST + item.find('h3', class_='proposition_name').find_next('a'). get('href')
        })
    return cars


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count +1):
            print(f'Парсинг страницы {page} из {pages_count}')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} машин')
    else:
        print('Error')


parse()