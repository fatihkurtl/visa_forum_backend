from rest_framework import serializers
from .models import Member, MemberRole, Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import uuid

class MemberRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberRole
        fields = ['role']
        
class MemberTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['token', 'expires_at']

class MemberSerializer(serializers.ModelSerializer):
    roles = MemberRoleSerializer(source='memberrole', read_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = '__all__'

    def get_tokens(self, obj):
        """Member için mevcut token'ları döndür."""
        tokens = obj.tokens.all()
        return MemberTokenSerializer(tokens, many=True).data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        fields = ['firstname', 'lastname', 'username', 'email', 'password', 'terms']

    def validate_email(self, value):
        """E-posta adresinin benzersiz olduğunu kontrol et."""
        if Member.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu e-posta adresi zaten kullanılıyor.")
        return value

    def validate_username(self, value):
        """Kullanıcı adının benzersiz olduğunu kontrol et."""
        if Member.objects.filter(username=value).exists():
            raise serializers.ValidationError("Bu kullanıcı adı zaten kullanılıyor.")
        return value

    def create(self, validated_data):
        """Yeni bir kullanıcı oluştur."""
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['ip_address'] = self.context['request'].META.get('REMOTE_ADDR')
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')
        user = None

        if '@' in identifier:
            user = Member.get_by_email(identifier)
        else:
            user = Member.objects.filter(username=identifier).first()

        if user is None:
            raise serializers.ValidationError("Geçersiz kullanıcı adı/e-posta veya şifre.")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Geçersiz kullanıcı adı/e-posta veya şifre.")

        token, created = Token.objects.get_or_create(member=user)
        if created:
            token.token = str(uuid.uuid4())
            token.save()

        return {
            'member': MemberSerializer(user).data,
            'token': token.token,
            'expires_at': token.expires_at
        }