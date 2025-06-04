# presentation/serializers/membresia_serializer.py
from rest_framework import serializers
from core.infrastructure.persistence.models.membresia import Membresia

class MembresiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membresia
        fields = '__all__'
