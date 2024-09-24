from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Thread
from .serializers import ThreadSerializer


class ThreadsView(APIView):
    def get(self, request, format=None):
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)