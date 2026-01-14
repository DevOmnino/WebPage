from django.urls import path
from .views import *

app_name = 'inbox'

urlpatterns = [
    path('', landing, name="landing"),
    path('acv_calculator/', acv_calculator, name="acv_calculator"),
    path('photo-verifier/', photo_verifier, name="photo_verifier"),
]