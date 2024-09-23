from django.contrib import admin
from .models import Member, MemberRole

class MemberRoleInline(admin.TabularInline):
    model = MemberRole
    extra = 1  # Yeni bir MemberRole eklemek için bir satır göster

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'firstname', 'lastname', 'username', 'email', 
        'is_active', 'email_verified', 'created_at'
    )  # Görüntülenecek alanlar
    search_fields = ('firstname', 'lastname', 'username', 'email')  # Arama yapılacak alanlar
    list_filter = ('is_active', 'email_verified')  # Filtreleme seçenekleri
    inlines = [MemberRoleInline]  # MemberRole'ları inline olarak göster

    # Form alanlarını özelleştirmek için
    fieldsets = (
        (None, {
            'fields': ('firstname', 'lastname', 'username', 'email', 'profile_image', 'password', 'bio', 'expertise', 'email_notifications', 'is_active')
        }),
        ('Permissions', {
            'fields': ('email_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),  # Bu alanlar düzenlenemez
            'classes': ('collapse',),  # Bu alanları çökertilebilir yap
        }),
    )

    # Bu alanları düzenlenebilir olmaktan çıkar
    readonly_fields = ('created_at', 'updated_at')  # readonly_fields ile bu alanları sadece okunur yap

@admin.register(MemberRole)
class MemberRoleAdmin(admin.ModelAdmin):
    list_display = ('member', 'role', 'created_at')  # Görüntülenecek alanlar
    search_fields = ('member__username', 'role')  # Arama yapılacak alanlar