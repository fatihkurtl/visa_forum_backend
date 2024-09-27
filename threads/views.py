from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Thread
from .serializers import CategorySerializer, ThreadSerializer


class ThreadsView(APIView):
    def get(self, request, format=None):
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ThreadsCategoriesView(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)