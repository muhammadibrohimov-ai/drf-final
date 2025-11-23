from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField()
    image = models.ImageField(upload_to='posts/')
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='posts')
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ('-updated_at',)
        db_table = 'post'
        

class Comment(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self,):
        return self.user.username
    
    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ('-updated_at',)
        db_table = 'comment'
        
        
class Chat(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'chat'
        verbose_name_plural = 'chats'
        ordering = ('-created_at',)
        db_table = 'chat'    
        
        
class UserRequest(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='user_requests')
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='user_requests') 
    text = models.TextField()
    image = models.ImageField(upload_to='requests/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'user_request'
        verbose_name_plural = 'user_requests'
        ordering = ('-created_at',)
        db_table = 'user_request'    
    
    
class AIresponse(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='ai_responses')
    user_request = models.ForeignKey('UserRequest', on_delete=models.CASCADE, related_name='responses')
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='ai_responses')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'ai_response'
        verbose_name_plural = 'ai_responses'
        ordering = ('-created_at',)
        db_table = 'ai_response'    
    
    