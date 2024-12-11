from django.shortcuts import render
from django.http import HttpResponse
from .models import MedicalDocument
from .utils import extract_text_from_pdf, extract_tables_from_pdf  # Функция извлечения текста

def upload_and_analyze(request):
    if request.method == 'POST' and request.FILES.get('medical-document'):
        uploaded_file = request.FILES['medical-document']
        
        # Проверяем формат файла
        if uploaded_file.content_type != 'application/pdf':
            return HttpResponse("Ошибка: можно загружать только PDF-файлы.")
        
        # Сохраняем документ
        doc = MedicalDocument(file=uploaded_file)
        doc.save()
        
        # Извлекаем текст из PDF
        extract_tables_from_pdf(uploaded_file)
        text = extract_text_from_pdf(uploaded_file)
        
        # Пример анализа текста: поиск ключевых слов
        if "диагноз" in text.lower():
            result = "Файл содержит ключевое слово 'диагноз'."
        else:
            result = "Ключевое слово 'диагноз' не найдено."
        
        return HttpResponse(f"Текст проанализирован. {result}")
    
    return render(request, 'index.html')
