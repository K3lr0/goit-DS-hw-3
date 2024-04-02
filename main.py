import requests
from bs4 import BeautifulSoup
import json

# Функція для отримання інформації про автора зі сторінки автора
def scrape_author_info(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    born_info = soup.find('span', class_='author-born-date').text
    born_location = soup.find('span', class_='author-born-location').text
    description = soup.find('div', class_='author-description').text.strip()
    return {'born_date': born_info, 'born_location': born_location, 'description': description}

# Функція для отримання цитат та їх авторів зі сторінки
def scrape_quotes(url):
    quotes = []
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            author_url = 'http://quotes.toscrape.com' + quote.find('a')['href']  # Отримуємо URL-адресу сторінки автора
            author_info = scrape_author_info(author_url)
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            quotes.append({'quote': text, 'author': author, 'tags': tags, **author_info})
        next_button = soup.find('li', class_='next')
        if not next_button:
            break
        url = 'http://quotes.toscrape.com' + next_button.find('a')['href']
    return quotes

# URL сайту, який ми скрапимо
base_url = 'http://quotes.toscrape.com'
# Отримуємо список цитат з усіх сторінок
quotes = scrape_quotes(base_url)

# Функція для отримання інформації про авторів
def scrape_authors(quotes):
    authors = {}
    for quote in quotes:
        if quote['author'] not in authors:
            authors[quote['author']] = {
                'fullname': quote['author'],
                'born_date': quote['born_date'],
                'born_location': quote['born_location'],
                'description': quote['description']
            }
    return list(authors.values())

# Отримуємо список унікальних авторів
authors = scrape_authors(quotes)

# Збереження цитат у JSON файл
with open('quotes.json', 'w') as f:
    json.dump(quotes, f, indent=2)

# Збереження інформації про авторів у JSON файл
with open('authors.json', 'w') as f:
    json.dump(authors, f, indent=2)

print("Дані успішно зібрано та збережено.")
