from rest_framework import serializers
from .models import Category, Thread, Comments, Replies


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_title', 'image', 'threads', 'created_at', 'updated_at']


class ThreadSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'category', 'author', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    thread = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'content', 'likes', 'replies', 'thread', 'author', 'created_at', 'updated_at']


class ReplySerializer(serializers.ModelSerializer):
    comment = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        model = Replies
        fields = ['id', 'content', 'likes', 'comment', 'author', 'created_at', 'updated_at']
