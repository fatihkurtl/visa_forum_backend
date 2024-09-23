from .models import Member
from .serializers import MemberSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MemberView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        # members = Member.objects.all()
        members = [
            {
                "name": "John",
                "lastname": "Doe",
                "username": "john",
                "email": "l2W9J@example.com",
            }
        ]
        # serializer = MemberSerializer(members, many=True)
        # return Response(serializer.data)
        return Response(members)

    # def post(self, request, format=None):
    #     serializer = MemberSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)