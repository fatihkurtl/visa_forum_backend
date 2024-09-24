from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name='Kategori adı')
    sub_title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Alt başlık')
    image = models.ImageField(upload_to='categories/images', null=True, blank=True, verbose_name='Kategori resmi')
    
    threads = models.ManyToManyField('Thread', blank=True, related_name='category_threads', verbose_name='Konular')
        
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.name
    

class Thread(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Başlık')
    content = models.TextField(null=False, blank=False, verbose_name='İçerik')
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategori')
    author = models.ForeignKey('members.Member', on_delete=models.CASCADE, verbose_name='Yazar')
    
    likes = models.ManyToManyField('members.Member', blank=True, related_name='thread_likes', verbose_name='Beğeniler')
    is_active = models.BooleanField(default=True, verbose_name='Aktif mi?')
    
    comments = models.ManyToManyField('Comments', blank=True, related_name='thread_comments', verbose_name='Yorumlar')
    
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
    
    likes = models.ManyToManyField('members.Member', blank=True, related_name='comment_likes', verbose_name='Beğeniler')
    replies = models.ManyToManyField('Replies', blank=True, null=True, related_name='comment_replies', verbose_name='Cevaplar')
    
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comment_threads', verbose_name='Konu')
    author = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='comment_author', verbose_name='Yazar')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yayın tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Yorum'
        verbose_name_plural = 'Yorumlar'

    def __str__(self):
        return self.content
    

class Replies(models.Model):
    content = models.TextField(null=False, blank=False, verbose_name='İçerik')
    
    likes = models.ManyToManyField('members.Member', blank=True, related_name='reply_likes', verbose_name='Beğeniler')
    
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='reply_comments', verbose_name='Yorum')
    author = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name='reply_author', verbose_name='Yazar')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yayın tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncelleme tarihi')
    
    class Meta:
        db_table = 'replies'
        verbose_name = 'Cevap'
        verbose_name_plural = 'Cevaplar'

    def __str__(self):
        return self.content