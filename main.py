import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


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


    for review_elem in review_elements:
        print(review_elem)
        print("_______________________________________________________________")

        rate = soup.find_all('div', class_="lb3db10af lb57a25cc")
        print(rate)             #selenium

        reviews.append({
            'Rating': rating,
            'Title': title,
            'Text': text,
            'Date': date,
            'Bank Reply': bank_reply
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
    reviews = get_all_reviews(base_url, num_pages=10)

    # Создаем DataFrame и сохраняем в Excel
    if reviews:
        df = pd.DataFrame(reviews)
        df.to_excel("psb_reviews.xlsx", index=False, engine='openpyxl')
        print("Данные сохранены в файл psb_reviews.xlsx")
    else:
        print("Отзывы не были получены.")
