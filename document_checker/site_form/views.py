from django.shortcuts import render
from django.http import HttpResponse
from .models import MedicalDocument

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('medical-document'):
        uploaded_file = request.FILES['medical-document']
        if uploaded_file.content_type == 'application/pdf':
            doc = MedicalDocument(file=uploaded_file)
            doc.save()
            return HttpResponse("Файл успешно загружен!")
        else:
            return HttpResponse("Неверный формат файла. Допускается только PDF.")
    return render(request, 'index.html')
