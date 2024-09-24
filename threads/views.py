from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ThreadsView(APIView):
    def get(self, request, format=None):
        threads = [
        {
            'id': 1,
            'title': 'Thread 1',
            'content': 'Thread 1 content'
        },
        {
            'id': 2,
            'title': 'Thread 2',
            'content': 'Thread 2 content'
        },
        {
            'id': 3,
            'title': 'Thread 3',
            'content': 'Thread 3 content'
        }
    ]
        return Response(threads, status=status.HTTP_200_OK)