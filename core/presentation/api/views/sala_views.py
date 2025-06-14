# src/presentation/api/views/sala_views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.infrastructure.persistence.models.sala import Sala
from core.presentation.serializers.sala_serializer import SalaSerializer

class SalaView(APIView):

    def get(self, request):
        salas = Sala.objects.all()
        data = SalaSerializer(salas, many=True).data
        
        if not salas:
            return Response({
                "mensaje": "No hay salas registradas"},
                status= status.HTTP_204_NO_CONTENT) # No hay registros
        
        return Response({
            "registros": data},
            status= status.HTTP_200_OK) # Sí hay registros


    def post(self, request):
        sala = SalaSerializer(data=request.data)
        
        if not sala.is_valid():
            return Response({
                        "mensaje": "Error al registrar sala",
                        "errores": sala.errors},
                        status= status.HTTP_400_BAD_REQUEST)
        
        sala.save()
        return Response({
            "nombre": sala.data['nombre'],
            "mensaje": "Se ha registrado la sala correctamente"},
            status= status.HTTP_201_CREATED)


    def put(self, request, pk):
        try:
            sala = Sala.objects.get(id=pk)
            serializer = SalaSerializer(sala, data=request.data)
            if not serializer.is_valid():
                return Response({
                    "mensaje": "Error al actualizar sala",
                    "errores": serializer.errors},
                    status= status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'mensaje': 'Sala actualizada correctamente',
                'Registro': serializer.data},
                status= status.HTTP_200_OK)
        
        except Sala.DoesNotExist:
            return Response({
                "mensaje": "Sala no encontrada"},
                status= status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk):
        try:
            obj = Sala.objects.get(id= pk)
            obj.delete()
            return Response({
                "id": pk,
                "nombre": obj.nombre,
                "mensaje": "Sala eliminada correctamente"},
                status= status.HTTP_204_NO_CONTENT)
        
        except:
            return Response({
                "mensaje":"Sala no encontrada"},
                status= status.HTTP_404_NOT_FOUND)

