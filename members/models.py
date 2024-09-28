from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import timedelta

class Member(models.Model):
    firstname = models.CharField(max_length=100, null=False, blank=False, verbose_name='Ad')
    lastname = models.CharField(max_length=100, null=False, blank=False, verbose_name='Soyad')
    username = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name='Kullanıcı adı')
    email = models.EmailField(null=False, blank=False, unique=True, verbose_name='E-posta adresi')
    profile_image = models.ImageField(upload_to='members/profile_images', null=True, blank=True, verbose_name='Profil resmi')
    password = models.CharField(max_length=100, null=False, blank=False, verbose_name='Şifre')
    terms = models.BooleanField(default=True, verbose_name='Forum kurallarını onayladı mı?')
    
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP adresi')
    
    email_verified = models.BooleanField(default=False, verbose_name='E-posta doğrulandı mı?')
    is_active = models.BooleanField(default=True, verbose_name='Aktif mi?')
    
    country_of_interest = models.CharField(max_length=100, null=True, blank=True, verbose_name='İlgilenilen ülke')
    bio = models.TextField(null=True, blank=True, verbose_name='Biyografi')
    email_notifications = models.BooleanField(default=True, verbose_name='E-posta bilgilendirmeleri')
    expertise = models.CharField(max_length=100, null=True, blank=True, verbose_name='Uzmanlık Alanı')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'members'
        verbose_name = 'Üye'
        verbose_name_plural = 'Üyeler'
    
    @classmethod
    def get_by_email(cls, email):
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None
        
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'memberrole'):
            MemberRole.objects.create(member=self, role=MemberRole.Roles.MEMBER)
    
    def check_password(self, raw_password):
        """Verilen şifreyi kontrol et."""
        return check_password(raw_password, self.password)


class MemberRole(models.Model):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderatör'
        MEMBER = 'member', 'Üye'

    member = models.OneToOneField(Member, on_delete=models.CASCADE, verbose_name='Üye', related_name='memberrole')
    role = models.CharField(max_length=100, choices=Roles.choices, verbose_name='Rol')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Rol ekleme tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'member_roles'
        verbose_name = 'Üye rol'
        verbose_name_plural = 'Üye rolleri'
        
    def __str__(self):
        return f'{self.member.username} - {self.role}'
    
    
    
class Token(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='Üye', related_name='tokens')
    token = models.CharField(max_length=255, unique=True, verbose_name='Token')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    expires_at = models.DateTimeField(verbose_name='Son Geçerlilik Tarihi')

    class Meta:
        db_table = 'member_tokens'
        verbose_name = 'Üye Tokeni'
        verbose_name_plural = 'Üye Tokenleri'

    def __str__(self):
        return f'Token for {self.member.username} - Expires at {self.expires_at}'

    def is_expired(self):
        """Token'ın süresinin dolup dolmadığını kontrol et."""
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        """Token oluşturulurken geçerlilik süresini ayarla."""
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=1)
        super().save(*args, **kwargs)