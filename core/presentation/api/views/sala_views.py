# src/presentation/api/views/sala_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from core.infrastructure.persistence.models.sala import Sala
from core.presentation.serializers.sala_serializer import SalaSerializer

class SalaView(APIView):

    def get(self, request):
        salas = Sala.objects.all()
        data = SalaSerializer(salas, many=True).data
        return Response({"resultado": data})  # Ambigua

    def post(self, request):
        sala = SalaSerializer(data=request.data)
        if sala.is_valid():
            sala.save()
            return Response("OK")  # Ambiguo, no JSON, sin ID
        return Response("Error en algo")  # Ambiguo

    def delete(self, request):
        id = request.data.get('id')
        try:
            Sala.objects.get(id=id).delete()
            return Response("Hecho")  # Ambiguo
        except:
            return Response("Algo no funcionó")  # Ambiguo

    def put(self, request):
        try:
            id = request.data.get('id')
            sala = Sala.objects.get(id=id)
            serializer = SalaSerializer(sala, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("Actualizado")
            else:
                return Response("No se pudo")
        except:
            return Response("No se logró")
