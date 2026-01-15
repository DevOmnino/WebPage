from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gradio_client import Client, handle_file
from .forms import ImageUploadForm, ACVForm
import os
import tempfile

# Create your views here.

def landing(request):
    return render(request, 'landing.html')

# @login_required
def home(request):
    return render(request, 'home.html')

def real_or_fake(uploaded_file):
    client = Client("DevOmnino/Test")
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1]
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
    return {
        "result": result,
        "filename": filename
    }

@login_required
def photo_verifier(request):
    result = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST)
        if form.is_valid():
            images = request.FILES.getlist('images')
            description = form.cleaned_data['description']
            date = form.cleaned_data['date']
            results = []

            for image in images:
                res = real_or_fake(image)
                results.append(res)
            result = results
    else:
        form = ImageUploadForm()
    context = {
        'form': form,
        'result': result
    }
    return render(request, 'photo_verifier.html', context)

def acv_calculator(request):
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
    
