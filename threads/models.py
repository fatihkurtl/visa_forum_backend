from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from members.models import Member


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name='Kategori adı')
    sub_title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Alt başlık')
    image = models.ImageField(upload_to='categories/images', null=True, blank=True, verbose_name='Kategori resmi')
    
    threads = models.ManyToManyField('Thread', blank=True, related_name='categories', verbose_name='Konular')
        
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.name
    

class Thread(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name='Başlık')
    content = models.TextField(null=False, blank=False, verbose_name='İçerik')
    
    author = models.ForeignKey('members.Member', on_delete=models.CASCADE, verbose_name='Yazar')
    likes = models.ManyToManyField('members.Member', blank=True, through='Like', related_name='thread_likes', verbose_name='Beğeniler')
    views = models.PositiveIntegerField(default=0, verbose_name='Okunma sayısı')
    
    is_active = models.BooleanField(default=True, verbose_name='Aktif mi?')
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads_category', verbose_name='Kategori')
    # comments = models.ManyToManyField('members.Member', blank=True, through='Comments', related_name='thread_comments', verbose_name='Yorumlar')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yayın tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'threads'
        verbose_name = 'Konu'
        verbose_name_plural = 'Konular'

    def __str__(self):
        return self.title


class Comments(models.Model):
    content = models.TextField(null=False, blank=False, verbose_name='İçerik')
    likes = models.ManyToManyField('members.Member', blank=True, through='Like', related_name='comment_likes', verbose_name='Beğeniler')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_comments', verbose_name='Konu')
    replies = models.ManyToManyField('Reply', blank=True, related_name='comment_replies', verbose_name='Yanıtlar')
    author = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='comment_author', verbose_name='Yazar')    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yayın tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'
            
    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}..."

class Reply(models.Model):
    content = models.TextField(null=False, blank=False, verbose_name='İçerik')
    likes = models.ManyToManyField('members.Member', blank=True, through='Like', related_name='reply_likes', verbose_name='Beğeniler')
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True, blank=True, related_name='reply_set', verbose_name='Yorum')
    author = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='reply_author', verbose_name='Yazar')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='Üst Yanıt')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yayın tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'replies'
        verbose_name = 'Yanıt'
        verbose_name_plural = 'Yanıtlar'
            
    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}..."

class Like(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='Üye')
    thread = models.ForeignKey('Thread', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Konu')
    comment = models.ForeignKey('Comments', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Yorum')
    reply = models.ForeignKey('Reply', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Yanıt')
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Beğenme tarihi')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Güncelleme tarihi')

    class Meta:
        db_table = 'likes'
        verbose_name = 'Beğeni'
        verbose_name_plural = 'Beğeniler'
        unique_together = ('member', 'thread', 'comment', 'reply')

    def __str__(self):
        return f"{self.member} liked {self.thread or self.comment or self.reply}"
    
    
