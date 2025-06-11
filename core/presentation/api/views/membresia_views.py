# presentation/api/views/membresia_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from core.infrastructure.persistence.models.membresia import Membresia
from core.presentation.serializers.membresia_serializer import MembresiaSerializer
from datetime import timedelta

class MembresiaView(APIView):

    def get(self, request):
        try:
            membresias = Membresia.objects.all()
            data = MembresiaSerializer(membresias, many=True).data # Sí hay registros
            
            if not data:
                return Response({"mensaje": "No hay membresias registradas"})
            
            return Response({"registros": data})
        
        except Membresia.DoesNotExist:
            return Response({"mensaje": "No hay membresias registradas"}) # No hay registros

    def post(self, request):
        data = request.data
        serializer = MembresiaSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({
                "mensaje": "Error al registrar membresía", 
                "errores": serializer.errors})
        
        serializer.save()
        return Response("Inscripción aceptada")  # Ambigua

    def put(self, request, pk):
        try:
            membresia = Membresia.objects.get(id=pk)
            serializer = MembresiaSerializer(membresia, data=request.data)
            if not serializer.is_valid():
                return Response({
                    "mensaje": "Error al actualizar membresía", 
                    "errores": serializer.errors
                })
        
            serializer.save()
            return Response({
                'mensaje': 'Membresía actualizada correctamente',
                'Registro':serializer.data})
        
        except Membresia.DoesNotExist:
            return Response({"mensaje": "Membresía no encontrada"})

    def delete(self, request, pk):
        try:
            obj = Membresia.objects.get(id=pk)
            obj.delete()
            return Response({
                "id": pk,
                "tipo": obj.tipo,
                "mensaje": "Membresia eliminada"
                })
        except Membresia.DoesNotExist:
            return Response({"mensaje": "Membresía no encontrada"})

class RenovarMembresiaView(APIView):
    def put(self, request, pk):
        
        try:
            obj = Membresia.objects.get(id=pk)
            if not obj.fecha_fin or not obj.fecha_inicio:
                return Response({"mensaje": "Fecha de inicio o fin no establecida"})
            
            obj.fecha_fin = obj.fecha_fin + timedelta(days=obj.duracion_dias)
            obj.save()
            return Response({
                "id": pk,
                "tipo": obj.tipo,
                "mensaje": "Membresía renovada correctamente",})
        
        except Membresia.DoesNotExist:
            return Response({"mensaje": "Membresía no encontrada"})


class AplicarPromocionView(APIView):
    def post(self, request):
        try:
            id = request.data.get("id")
            obj = Membresia.objects.get(id=id)
            obj.promocion = True
            obj.precio = obj.precio * 0.85  # Descuento del 15%
            obj.save()
            return Response("Con descuento")
        except:
            return Response("Error")
