from rest_framework import serializers
from .models import Category, Thread, Comments, Replies, Member

class CategorySerializer(serializers.ModelSerializer):
    threads = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_title', 'image', 'threads', 'created_at', 'updated_at']
        
    def get_threads(self, obj):
        from threads.serializers import ThreadSerializer
        return ThreadSerializer(obj.threads.all(), many=True).data

class ReplySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Replies
        fields = ['id', 'content', 'author', 'likes', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    replies = ReplySerializer(many=True, read_only=True, source='reply_comments')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id', 'content', 'likes_count', 'replies', 'author', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

class ThreadSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True, source='threads')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'category', 'author', 'likes_count', 'comments', 'is_active', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['title', 'content', 'category', 'author']

    def create(self, validated_data):
        return Thread.objects.create(**validated_data)