# src/presentation/serializers/sala_serializer.py
from rest_framework import serializers
from core.infrastructure.persistence.models.sala import Sala

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'
