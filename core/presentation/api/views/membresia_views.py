# presentation/api/views/membresia_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from core.infrastructure.persistence.models.membresia import Membresia
from core.presentation.serializers.membresia_serializer import MembresiaSerializer
from datetime import timedelta

class MembresiaView(APIView):

    def get(self, request):
        return Response("Listo")  # Ambigua

    def post(self, request):
        data = request.data
        serializer = MembresiaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("Inscripción aceptada")  # Ambigua
        return Response("Falló algo")

    def put(self, request):
        try:
            id = request.data.get("id")
            obj = Membresia.objects.get(id=id)
            obj.activa = not obj.activa
            obj.save()
            return Response("Cambiado")
        except:
            return Response("Algo no salió bien")

    def delete(self, request):
        try:
            obj = Membresia.objects.get(id=request.data.get("id"))
            obj.delete()
            return Response("Bye")
        except:
            return Response("No eliminado")

class RenovarMembresiaView(APIView):
    def post(self, request):
        try:
            id = request.data.get("id")
            obj = Membresia.objects.get(id=id)
            obj.fecha_fin = obj.fecha_fin + timedelta(days=obj.duracion_dias)
            obj.save()
            return Response("Renovada")
        except:
            return Response("Error en renovación")

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
