from rest_framework import serializers
from .models import Category, Reply, Thread, Comments, Member

class CategorySerializer(serializers.ModelSerializer):
    threads = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'sub_title', 'image', 'threads', 'created_at', 'updated_at']
        
    def get_threads(self, obj):
        from threads.serializers import ThreadSerializer
        return ThreadSerializer(obj.threads.all(), many=True).data
    
    def add_thread(self, obj):
        from threads.serializers import ThreadSerializer
        return ThreadSerializer(obj.threads.all(), many=True).data

class ReplySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = ['id', 'content', 'likes_count', 'author', 'created_at', 'updated_at', 'parent', 'children']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_children(self, obj):
        children = obj.children.all()
        return ReplySerializer(children, many=True).data

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    thread = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['thread', 'id', 'content', 'likes_count', 'author', 'created_at', 'updated_at', 'replies']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_thread(self, obj):
        return obj.thread.id if obj.thread else None

    def get_replies(self, obj):
        top_level_replies = obj.reply_set.filter(parent=None)
        return ReplySerializer(top_level_replies, many=True).data

class ThreadSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True, source='thread_comments')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'category', 'views', 'author', 'likes_count', 'is_active', 'created_at', 'updated_at', 'comments']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_author(self, obj):
        return obj.author

class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'category', 'author']

    def create(self, validated_data):
        return Thread.objects.create(**validated_data)