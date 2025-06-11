from django.urls import path
from core.presentation.api.views.membresia_views import (
    MembresiaView,
    RenovarMembresiaView,
    AplicarPromocionView,
)

urlpatterns = [
    path('membresias/', MembresiaView.as_view()),
    path('membresias/<int:pk>/', MembresiaView.as_view()),
    path('membresias/renovar/<int:pk>/', RenovarMembresiaView.as_view()),
    path('membresias/promocion/', AplicarPromocionView.as_view()),
]
