# Generated by Django 5.1.1 on 2024-10-04 00:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("threads", "0004_alter_reply_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="thread",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="threads_category",
                to="threads.category",
                verbose_name="Kategori",
            ),
        ),
    ]
