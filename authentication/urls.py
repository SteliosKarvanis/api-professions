from django.shortcuts import redirect
from django.urls import path
from .views import *

urlpatterns = [
    path('', lambda req: redirect('input/')),
    path('show/new_search', lambda req: redirect('/')),
    path('input/new_search', lambda req: redirect('/')),
    path('input/', input_profession, name="input"),
    path('show/', show_data, name="show"),
]