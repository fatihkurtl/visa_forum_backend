# Generated by Django 5.1.1 on 2024-09-25 20:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0009_member_terms"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="ip_address",
            field=models.GenericIPAddressField(
                blank=True, null=True, verbose_name="IP adresi"
            ),
        ),
    ]