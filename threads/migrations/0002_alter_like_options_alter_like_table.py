# Generated by Django 5.1.1 on 2024-09-26 21:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("threads", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="like",
            options={"verbose_name": "Beğeni", "verbose_name_plural": "Beğeniler"},
        ),
        migrations.AlterModelTable(
            name="like",
            table="likes",
        ),
    ]