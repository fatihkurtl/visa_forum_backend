# Generated by Django 5.1.1 on 2024-09-27 23:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firstname", models.CharField(max_length=100, verbose_name="Ad")),
                ("lastname", models.CharField(max_length=100, verbose_name="Soyad")),
                (
                    "username",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Kullanıcı adı"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="E-posta adresi"
                    ),
                ),
                (
                    "profile_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="members/profile_images",
                        verbose_name="Profil resmi",
                    ),
                ),
                ("password", models.CharField(max_length=100, verbose_name="Şifre")),
                (
                    "terms",
                    models.BooleanField(
                        default=True, verbose_name="Forum kurallarını onayladı mı?"
                    ),
                ),
                (
                    "ip_address",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="IP adresi"
                    ),
                ),
                (
                    "email_verified",
                    models.BooleanField(
                        default=False, verbose_name="E-posta doğrulandı mı?"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Aktif mi?"),
                ),
                (
                    "country_of_interest",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="İlgilenilen ülke",
                    ),
                ),
                (
                    "bio",
                    models.TextField(blank=True, null=True, verbose_name="Biyografi"),
                ),
                (
                    "email_notifications",
                    models.BooleanField(
                        default=True, verbose_name="E-posta bilgilendirmeleri"
                    ),
                ),
                (
                    "expertise",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Uzmanlık Alanı",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Kayıt tarihi"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Güncelleme tarihi"
                    ),
                ),
            ],
            options={
                "verbose_name": "Üye",
                "verbose_name_plural": "Üyeler",
                "db_table": "members",
            },
        ),
        migrations.CreateModel(
            name="MemberRole",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("admin", "Admin"),
                            ("moderator", "Moderatör"),
                            ("member", "Üye"),
                        ],
                        max_length=100,
                        verbose_name="Rol",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Rol ekleme tarihi"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Güncelleme tarihi"
                    ),
                ),
                (
                    "member",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberrole",
                        to="members.member",
                        verbose_name="Üye",
                    ),
                ),
            ],
            options={
                "verbose_name": "Üye rol",
                "verbose_name_plural": "Üye rolleri",
                "db_table": "member_roles",
            },
        ),
        migrations.CreateModel(
            name="Token",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "token",
                    models.CharField(max_length=255, unique=True, verbose_name="Token"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
                    ),
                ),
                (
                    "expires_at",
                    models.DateTimeField(verbose_name="Son Geçerlilik Tarihi"),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tokens",
                        to="members.member",
                        verbose_name="Üye",
                    ),
                ),
            ],
            options={
                "verbose_name": "Üye Tokeni",
                "verbose_name_plural": "Üye Tokenleri",
                "db_table": "member_tokens",
            },
        ),
    ]
