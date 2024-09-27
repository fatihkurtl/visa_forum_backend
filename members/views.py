from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MemberSerializer, LoginSerializer, RegisterSerializer
from .models import Member


###! FOR API TEST
class MemberView(APIView):
    def get(self, request, format=None):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView): ###! buradaki suggestion'u cookie veya local storage olarak kayit edip loginde veya ana sayfada kullanıcıya goster.
    
    SUGGESTIONS = ['E-posta adresinizi onaylayın.', 'Hesabınıza giriş yapın.', 'Profil bilgilerinizi güncelleyin.']
    
    def post(self, request, format=None):
        member_ip = request.META.get('REMOTE_ADDR')
        print(member_ip)
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Başarıyla kayıt olundu.', 'suggestions': self.SUGGESTIONS, 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request, format=None):
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    

class MemberDetailView(APIView):
    
    SUGGESTIONS = ['E-posta adresinizi onaylayın.', 'Hesabınıza giriş yapın.']
    
    def get_object(self, username):
        try:
            return Member.objects.get(username=username)
        except Member.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, username, format=None):
        member = self.get_object(username)
        serializer = MemberSerializer(member)
        if serializer.data is None:
            return Response({'message': 'Kullanıcı bulunamadı.', 'suggestions': self.SUGGESTIONS}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)