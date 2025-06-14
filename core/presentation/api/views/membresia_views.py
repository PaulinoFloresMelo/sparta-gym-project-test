# presentation/api/views/membresia_views.py
from decimal import Decimal
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.infrastructure.persistence.models.membresia import Membresia
from core.presentation.serializers.membresia_serializer import MembresiaSerializer
from datetime import timedelta

class MembresiaView(APIView):

    def get(self, request):
        membresias = Membresia.objects.all()
        data = MembresiaSerializer(membresias, many=True).data
        
        if not data:
            return Response({
                "mensaje": "No hay membresias registradas"},
                status=status.HTTP_204_NO_CONTENT) # Si hay registros
        
        return Response({"registros": data}) # Sí hay registros


    def post(self, request):
        membresia = MembresiaSerializer(data=request.data)
        
        if not membresia.is_valid():
            return Response({
                "mensaje": "Error al registrar la membresía", 
                "errores": membresia.errors},
                status=status.HTTP_400_BAD_REQUEST)
        
        membresia.save()
        return Response({
            "tipo": membresia.data['tipo'],
            "mensaje":"Se ha registrado la membresía correctamente"}, 
            status=status.HTTP_201_CREATED) # Registro exitoso


    def put(self, request, pk):
        try:
            membresia = Membresia.objects.get(id=pk)
            serializer = MembresiaSerializer(membresia, data=request.data)
            if not serializer.is_valid():
                return Response({
                    "mensaje": "Error al actualizar membresía", 
                    "errores": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)
        
            serializer.save()
            return Response({
                'mensaje': 'Membresía actualizada correctamente',
                'Registro':serializer.data},
                status=status.HTTP_200_OK) # Actualización exitosa
        
        except Membresia.DoesNotExist:
            return Response({
                "mensaje": "Membresía no encontrada"},
                status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk):
        try:
            obj = Membresia.objects.get(id=pk)
            obj.delete()
            return Response({
                "id": pk,
                "tipo": obj.tipo,
                "mensaje": "Membresia eliminada correctamente"},
                status=status.HTTP_204_NO_CONTENT) # Eliminación exitosa

        except Membresia.DoesNotExist:
            return Response({
                "mensaje": "Membresía no encontrada"},
                status=status.HTTP_404_NOT_FOUND)

class RenovarMembresiaView(APIView):
    
    def put(self, request, pk):
        try:
            obj = Membresia.objects.get(id=pk)
            if not obj.fecha_fin or not obj.fecha_inicio:
                return Response({
                    "tipo": obj.tipo,
                    "mensaje": "Fecha de inicio o fin no establecida"},
                    status=status.HTTP_400_BAD_REQUEST)
            
            obj.fecha_fin = obj.fecha_fin + timedelta(days=obj.duracion_dias)
            obj.save()
            return Response({
                "id": pk,
                "tipo": obj.tipo,
                "mensaje": "Membresía renovada correctamente"},
                status=status.HTTP_200_OK) # Renovación exitosa
        
        except Membresia.DoesNotExist:
            return Response({
                "mensaje": "Membresía no encontrada"},
                status=status.HTTP_404_NOT_FOUND)


class AplicarPromocionView(APIView):
    
    def put(self, request, pk):
        try:
            obj = Membresia.objects.get(id=pk)
            obj.promocion = True
            obj.precio = obj.precio * Decimal(0.85)  # Descuento del 15%
            obj.save()
            return Response({
                "id": pk,
                "tipo": obj.precio,
                "mensaje": "Promoción aplicada correctamente"},
                status=status.HTTP_200_OK)  # Promoción aplicada exitosamente
        
        except Membresia.DoesNotExist:
            return Response({
                "mensaje": "Membresía no encontrada"},
                status=status.HTTP_404_NOT_FOUND)
