# Generated by Django 5.1.1 on 2024-09-24 19:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("threads", "0006_remove_comments_replies_comments_replies"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comments",
            name="replies",
        ),
        migrations.RemoveField(
            model_name="thread",
            name="comments",
        ),
    ]
