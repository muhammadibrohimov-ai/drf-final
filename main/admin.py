from django.contrib import admin
from .models import Post, Comment, Chat, UserRequest, AIresponse

# Register your models here.


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'views', 'likes', 'updated_at']
    list_display_links = ['title', 'user', 'views', 'likes', 'updated_at']
    search_fields = ['title', 'user', 'desc']
    list_filter = ['user']
    ordering = ['-views']
    

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'likes']
    list_display_links = ['post', 'user', 'likes']
    search_fields = ['user', 'post', 'text']
    list_filter = ['user', 'post']
    ordering = ['-likes']
    

@admin.register(Chat)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'created_at']
    list_display_links = ['user', 'name', 'created_at']
    search_fields = ['user', 'name']
    list_filter = ['user']
    ordering = ['-created_at']
    

@admin.register(UserRequest)
class UserRequestModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'chat', 'created_at']
    list_display_links = ['user', 'chat', 'created_at']
    search_fields = ['user', 'chat', 'text', 'image']
    list_filter = ['user', 'chat']
    ordering = ['-created_at']
    
    
@admin.register(AIresponse)
class AIresponseModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_request', 'chat', 'created_at']
    list_display_links = ['user', 'user_request', 'chat', 'created_at']
    list_filter = ['user', 'chat', 'user_request']
    search_fields = ['user', 'chat', 'user_request', 'text']
    ordering = ['-created_at']
    
    
    
