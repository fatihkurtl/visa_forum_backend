from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from members.models import Member, Token
from members.serializers import MemberTokenSerializer
from .models import Category, Comments, Thread
from .serializers import CategorySerializer, ThreadSerializer, ThreadCreateSerializer


class ThreadsView(APIView):
    pagination_class = PageNumberPagination
    def get(self, request, format=None):
        threads = Thread.objects.all().order_by('-created_at')
        page = self.pagination_class().paginate_queryset(threads, request)
        if page is not None:
            serializer = ThreadSerializer(page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ThreadsCategoriesView(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ThreadsCreateView(APIView):
    def post(self, request, format=None):
        member_token = request.headers.get('Authorization').split(' ')[1]
        member = MemberTokenSerializer().check_token(member_token)            
        title = request.data.get('title')
        content = request.data.get('content')
        selected_category = Category.objects.get(pk=int(request.data.get('category')))
        author = Member.objects.get(pk=member.pk)

        if member is None:
            return Response({'message': 'Geçersiz token.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not title or not content or not selected_category:
            return Response({'message': 'Eksik bilgi.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = ThreadCreateSerializer(data={'title': title, 'content': content, 'category': selected_category.pk, 'author': author.pk})
        if serializer.is_valid():
            serializer.save()
            save_category = selected_category.threads.add(Thread.objects.get(pk=serializer.data.get('id')))
            print(save_category)
            return Response({"token": member.token, "expires_at": member.expires_at}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)