from rest_framework import serializers
from .models import Member, MemberRole, Token
from django.contrib.auth import authenticate
import uuid

class MemberRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberRole
        fields = ['role']
        
class MemberTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['token', 'expires_at']  # Token ve geçerlilik süresi

class MemberSerializer(serializers.ModelSerializer):
    roles = MemberRoleSerializer(source='memberrole', read_only=True)
    tokens = serializers.SerializerMethodField()  # Token'ları almak için özel bir alan

    class Meta:
        model = Member
        fields = '__all__'

    def get_tokens(self, obj):
        """Member için mevcut token'ları döndür."""
        tokens = obj.tokens.all()  # Tüm token'ları al
        return MemberTokenSerializer(tokens, many=True).data  # Token'ları serialize et

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # Kullanıcı adı veya e-posta
    password = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        # Kullanıcıyı doğrula (kullanıcı adı veya e-posta ile)
        user = None
        if '@' in identifier:  # E-posta kontrolü
            user = Member.get_by_email(identifier)  # E-posta ile kullanıcıyı al
        else:  # Kullanıcı adı ile doğrulama
            user = authenticate(username=identifier, password=password)

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Geçersiz kullanıcı adı/e-posta veya şifre.")

        # Token oluştur
        token, created = Token.objects.get_or_create(member=user)
        if created:
            token.token = str(uuid.uuid4())  # Benzersiz bir token oluştur
            token.save()

        return {
            'member': MemberSerializer(user).data,
            'token': token.token,
            'expires_at': token.expires_at
        }