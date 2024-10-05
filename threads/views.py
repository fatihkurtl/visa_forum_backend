from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from members.models import Member, Token
from members.serializers import MemberTokenSerializer
from .models import Category, Comments, Reply, Thread
from .serializers import CategorySerializer, ThreadSerializer, ThreadCreateSerializer


class ThreadsView(APIView):
    def get(self, request, format=None):
        threads = Thread.objects.filter(is_active=True).order_by('-created_at')
        if threads is not None:
            serializer = ThreadSerializer(threads, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Konu bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)
    

class ThreadsDetailView(APIView):
    def get(self, request, pk, format=None):
        thread = Thread.objects.filter(is_active=True, pk=pk).first()
        print(thread)
        if thread is not None:
            author = Member.objects.get(pk=thread.author.pk)
            print(author.firstname, author.lastname)
            serializer = ThreadSerializer(thread)           
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Konu bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)
    

class ThreadsCategoriesView(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all().order_by('-created_at')
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
    

class ThreadsAddCommentView(APIView):
    def post(self, request, pk, format=None):
        member_token = request.headers.get('Authorization').split(' ')[1]
        member = MemberTokenSerializer().check_token(member_token)            
        thread = Thread.objects.get(pk=request.data.get('thread_id'))
        content = request.data.get('content')
        author = Member.objects.get(pk=member.pk)
    
        print(request.data)
        print(member_token)
        print(pk)
        print(thread)
        print(content)
        print(author)
        if member is None:
            return Response({'message': 'Geçersiz token.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not content:
            return Response({'message': 'Eksik bilgi.'}, status=status.HTTP_400_BAD_REQUEST)
        
        save_comment = Comments.objects.create(thread=thread, content=content, author=author)
        print(save_comment)
        return Response({'message': 'Yorum kaydedildi.', 'status': 'success'}, status=status.HTTP_201_CREATED)
    

class ThreadsAddReplyView(APIView):
    def post(self, request, pk, format=None):
        member_token = request.headers.get('Authorization').split(' ')[1]
        member = MemberTokenSerializer().check_token(member_token)    
        comment = Comments.objects.get(pk=request.data.get('parent_id'))
        print(member_token)
        print(comment)
        print(request.data)
        # content = request.data.get('content')
        # author = Member.objects.get(pk=member.pk)
    
        # if member is None:
        #     return Response({'message': 'Geçersiz token.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # if not content:
        #     return Response({'message': 'Eksik bilgi.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # save_reply = Reply.objects.create(thread=comment.thread, content=content, author=author, reply_to=comment)
        # print(save_reply)
        return Response({'message': 'Yorum kaydedildi.', 'status': 'success'}, status=status.HTTP_201_CREATED)