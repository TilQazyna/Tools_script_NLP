import requests
from bs4 import BeautifulSoup

# Функция для извлечения ссылок с одной страницы
def extract_links_from_page(page_num):
    url = f"https://qazaquni.kz/public/kogam/page/{page_num}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Не удалось загрузить страницу {page_num}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    # Находим все контейнеры с классом 'news-list-item'
    items = soup.find_all('div', class_='news-list-item')
    
    links = []
    
    # Ищем все ссылки в этих контейнерах
    for item in items:
        link_tag = item.find('a', href=True)
        if link_tag:
            links.append(link_tag['href'])

    return links

# Функция для извлечения ссылок с нескольких страниц
def extract_links_from_pages(start_page, end_page):
    all_links = []
    for page in range(start_page, end_page + 1):
        print(f"Парсинг страницы {page}")
        links = extract_links_from_page(page)
        all_links.extend(links)
    
    return all_links

# Извлекаем ссылки с первой по последнюю страницу (1 до 317)
start_page = 1
end_page = 868

all_links = extract_links_from_pages(start_page, end_page)

# Сохраняем ссылки в файл
with open("qazaquni_kogam_list_item_links.txt", "w") as f:
    for link in all_links:
        f.write(f"{link}\n")

print(f"Извлечено {len(all_links)} ссылок")
