from PyPDF2 import PdfReader
import pdfplumber

import json
from fuzzywuzzy import fuzz

import requests
import json

def extract_text_from_pdf(pdf_file):
    """
    Извлечение текста из PDF-файла.
    """
    reader = PdfReader(pdf_file)  # Открываем файл
    text = ""

    for page in reader.pages:  # Проходим по всем страницам
        text += page.extract_text()  # Извлекаем текст из каждой страницы

   # print(text)
    return text

def extract_tables_from_pdf(pdf_file):
    """
    Извлечение таблиц из PDF-файла.
    :param pdf_file: Путь к файлу PDF или объект файла.
    :return: Список таблиц (каждая таблица — список списков).
    """
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            table = page.extract_table()  # Извлекаем таблицу с текущей страницы
            if table:
                print(f"Таблица найдена на странице {page_number}")
                tables.append(table)
                print(table)
    return tables

# Загружаем данные из JSON-файла
def load_disease_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Функция для поиска наиболее подходящего статуса
def find_potential_status(diseases, query, threshold=70):
    """
    Находит наиболее подходящий статус по ключевым словам диагноза.
    
    :param diseases: Список заболеваний в формате [{keyword, status}, ...].
    :param query: Строка с диагнозом для проверки.
    :param threshold: Порог схожести (от 0 до 100).
    :return: Подходящий статус или сообщение о том, что статус не найден.
    """
    best_match = None
    best_score = 0

    for disease in diseases:
        # Сравниваем ключевые слова с диагнозом
        similarity = fuzz.token_set_ratio(query.lower(), disease['keyword'].lower())
        if similarity > best_score and similarity >= threshold:
            best_match = disease
            best_score = similarity
    
    if best_match:
        return {
            "status": best_match['status'],
            "similarity": best_score,
            "matched_keyword": best_match['keyword']
        }
    else:
        return {"message": "Статус не найден. Попробуйте уточнить диагноз."}


def load_json_from_google_drive(file_id):
    """
    Загрузка JSON-файла из Google Диска по его ID.
    :param file_id: Идентификатор файла Google Drive.
    :return: Словарь с данными JSON.
    """
    # 1YbzJW_WSVW_evobKcBmwxtnyrb61hdL7
    base_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    response = requests.get(base_url)
    if response.status_code == 200:
        print(response.json)
        try:
            return response.json()  # Возвращаем загруженные данные в формате JSON
        except json.JSONDecodeError:
            raise ValueError("Файл не содержит корректный JSON.")
    else:
        raise ConnectionError(f"Не удалось загрузить файл. Код ответа: {response.status_code}")

