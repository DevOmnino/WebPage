from django.shortcuts import render
from gradio_client import Client, handle_file
from .forms import ImageUploadForm, ACVForm
import os
import tempfile

# Create your views here.

def home(request):
    return render(request, 'index.html')

def real_or_fake(uploaded_file):
    client = Client("DevOmnino/Test")

    ext = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        temp_path = temp_file.name

    try:
        result = client.predict(
            image=handle_file(temp_path),
            api_name="/predict"
        )
    finally :
        os.remove(temp_path)
    return result

def claims(request):
    result = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            description = form.cleaned_data['description']
            date = form.cleaned_data['date']
            result = real_or_fake(image)
    else:
        form = ImageUploadForm()
    # result = real_or_fake("/workspaces/WebPage/static/images/real-image2.jpg")
    context = {
        'form': form,
        'result': result
    }
    return render(request, 'model.html', context)

def calculate_acv(request):
    acv = None
    original_cost = None
    age = None
    useful_life = None
    depreciation_rate = None
    total_depreciation = None

    if request.method == 'POST':
        form = ACVForm(request.POST)
        if form.is_valid():
            original_cost = form.cleaned_data['original_cost']
            age = form.cleaned_data['age']
            useful_life = form.cleaned_data['useful_life']

            depreciation_rate = 100 / useful_life
            total_depreciation = (original_cost / useful_life) * age
            acv = original_cost - total_depreciation
    else:
        form = ACVForm()
    context = {
        'form': form,
        'original_cost': original_cost,
        'age': age,
        'useful_life': useful_life,
        'depreciation_rate': depreciation_rate,
        'total_depreciation': total_depreciation,
        'acv': acv
    }
    return render(request, 'acv_calculator.html', context)
    
