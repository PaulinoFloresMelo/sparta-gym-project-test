# src/presentation/api/urls/sala_urls.py
from django.urls import path
from core.presentation.api.views.workshop06_views import (
    activity_one, 
    activity_two,
    activity_three,
    activity_four,
    activity_five,
    activity_six
    )

urlpatterns = [
    path('workshop06/activity01/', activity_one()),
    path('workshop06/activity02/', activity_two()),
    path('workshop06/activity03/', activity_three()),
    path('workshop06/activity04/', activity_four()),
    path('workshop06/activity05/', activity_five()),
    path('workshop06/activity06/', activity_six()),
]
