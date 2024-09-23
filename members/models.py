from django.db import models
from django.contrib.auth.hashers import make_password

class Member(models.Model):
    firstname = models.CharField(max_length=100, null=False, blank=False, verbose_name='Ad')
    lastname = models.CharField(max_length=100, null=False, blank=False, verbose_name='Soyad')
    username = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name='Kullanıcı adı')
    email = models.EmailField(null=False, blank=False, unique=True, verbose_name='E-posta adresi')
    profile_image = models.ImageField(upload_to='members/profile_images', null=True, blank=True, verbose_name='Profil resmi')
    password = models.CharField(max_length=100, null=False, blank=False, verbose_name='Şifre')
    email_verified = models.BooleanField(default=False, verbose_name='E-posta doğrulandı mı?')
    is_active = models.BooleanField(default=True, verbose_name='Aktif mi?')
    
    bio = models.TextField(null=True, blank=True, verbose_name='Biyografi')
    email_notifications = models.BooleanField(default=True, verbose_name='E-posta bilgilendirmeleri')
    expertise = models.CharField(max_length=100, null=True, blank=True, verbose_name='Uzmanlık Alanı')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'members'
        verbose_name = 'Üye'
        verbose_name_plural = 'Üyeler'
        
    def __str__(self):
        return f'{self.firstname} {self.lastname} - {self.username} ({self.email})'
    
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
        if not self.memberrole_set.exists():
            MemberRole.objects.create(member=self, role=MemberRole.Roles.MEMBER)


class MemberRole(models.Model):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'
        MEMBER = 'member', 'Member'

    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='Üye')
    role = models.CharField(max_length=100, choices=Roles.choices, verbose_name='Rol')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Rol ekleme tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'member_roles'
        verbose_name = 'Üye rol'
        verbose_name_plural = 'Üye rolleri'
        
    def __str__(self):
        return f'{self.member.username} - {self.role}'