import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os

# Функция для загрузки HTML страницы
def download_html(url, output_dir, index):
    filename = os.path.join(output_dir, f"page_{index + 1}.html")
    try:
        response = requests.get(url, timeout=10)  # Добавлен тайм-аут
        response.raise_for_status()  # Проверка на успешность запроса
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        return f"Скачано: {url}"
    except requests.exceptions.RequestException as e:
        return f"Ошибка: {url}: {e}"

# Основная функция для загрузки страниц с прогрессом
def download_pages(input_file, output_dir):
    # Убедимся, что директория для сохранения существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Открываем файл со списком ссылок
    with open(input_file, 'r') as file:
        links = [link.strip() for link in file.readlines() if link.strip()]

    # Используем многопоточность для ускорения
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_html, link, output_dir, i) for i, link in enumerate(links)]

        # Отслеживаем прогресс с помощью tqdm
        for future in tqdm(as_completed(futures), total=len(futures), desc="Загрузка страниц"):
            result = future.result()
            print(result)

# Пример использования
input_file = r'D:\1 млрд есеп\Bauyrzhan\qazaquni.kz\qazaquni_kogam_list_item_links.txt'  # Ваш файл с ссылками
output_dir = r'D:\1 млрд есеп\Bauyrzhan\qazaquni.kz\қоғам'  # Укажите директорию для сохранения файлов

download_pages(input_file, output_dir)
