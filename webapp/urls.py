from django.urls import path
from .views import *

app_name = 'inbox'

urlpatterns = [
    path('', home, name="home"),
    path('claims/', claims, name="claims"),
    path('calculate_acv/', calculate_acv, name="calculate_acv"),
]