from rest_framework import serializers
from accounts.models import CustomUser
from .models import Post, Comment, Chat, UserRequest, AIresponse

# Create your serializers here.

        
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        quryset = CustomUser.objects.all()
    )
    post = serializers.PrimaryKeyRelatedField(
        queryset = Post.objects.all()
    )
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'views', 'likes', 'created_at', 'updated_at']
    

    
class PostSerializer(serializers.ModelSerializer):
    comments = 

