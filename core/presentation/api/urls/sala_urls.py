# src/presentation/api/urls/sala_urls.py
from django.urls import path
from core.presentation.api.views.sala_views import SalaView

urlpatterns = [
    path('salas/', SalaView.as_view()),
]
