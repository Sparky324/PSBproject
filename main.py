import json
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from html import unescape


# Функция для парсинга отзывов с одной страницы
def parse_reviews_page(url):
    reviews = []
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка загрузки страницы: {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    #print(soup)

    # Находим все элементы с отзывами на странице
    review_elements = soup.find_all('div', class_="la8a5ef73")

    rate = soup.find_all('div', class_="lb3db10af lb57a25cc")
    titl = soup.find_all('a', class_="link-simple")
    txt = soup.find_all('div', class_="l22dd3882")
    dat = soup.find_all('span', class_="l0caf3d5f")

    #print(dat[0].text.strip())
    #print(txt[0].find('a')['href'])

    for i in range(len(txt)):
        response1 = requests.get("https://www.banki.ru" + txt[i].find('a')['href'])
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        #print("https://www.banki.ru" + txt[i].find('a')['href'])
        data = json.loads(re.sub(r'[\x00-\x1f\x7f]', '', soup1.find('script', type="application/ld+json").string))
        #print(data)
        #print(soup1.find('script', type="application/ld+json"))

        #print(len(txt))

        reviews.append({
            'Rating': data['reviewRating']['ratingValue'],
            'Title': data['name'],
            'Text': unescape(data['author']['reviewBody']).replace('<p>', '').replace('</p>', '').replace('<ul>', '').replace('<li>', '').replace('</li>', '').replace('</ul>', ''),
            #'Date': date,
        })

    return reviews


# Функция для получения отзывов с нескольких страниц
def get_all_reviews(base_url, num_pages=5):
    all_reviews = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}?page={page}&is_countable=on"
        print(f"Парсинг страницы {page}...")
        reviews = parse_reviews_page(url)
        all_reviews.extend(reviews)
        time.sleep(2)  # Чтобы не перегружать сервер

    return all_reviews


# Основной код для парсинга отзывов
if __name__ == "__main__":
    # URL страницы отзывов банка ПСБ
    base_url = "https://www.banki.ru/services/responses/bank/promsvyazbank/"

    # Получаем все отзывы с нескольких страниц
    reviews = get_all_reviews(base_url, num_pages=1)

    # Создаем DataFrame и сохраняем в Excel
    if reviews:
        df = pd.DataFrame(reviews)
        df.to_excel("psb_reviews.xlsx", index=False, engine='openpyxl')
        print("Данные сохранены в файл psb_reviews.xlsx")
    else:
        print("Отзывы не были получены.")
