from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import Post, Comment, Chat, UserRequest, AIresponse

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Create your serializers here.

class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'password': self.user.password
        }
        data['success'] = True
        return data

    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
        
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all()
    )
    post = serializers.PrimaryKeyRelatedField(
        queryset = Post.objects.all()
    )
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'likes', 'created_at', 'updated_at']
    
    def validate_text(self, text):
        if not text:
            raise serializers.ValidationError("Text field cannot be empty")
        
        return text
    
    
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all()
    )
    image = serializers.ImageField(required = False)
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'views', 'likes', 'created_at', 'updated_at']

    def validate(self, attrs):
        title = (attrs.get('title') or "").strip().lower()
        desc = (attrs.get('desc') or "").strip()
        
        if not title:
            raise serializers.ValidationError("Title cannot be empty!")

        if self.instance:
            qs = Post.objects.filter(title=title).exclude(pk=self.instance.pk) 
        else:
            qs = Post.objects.filter(title=title)
            
        if qs.exists():
            raise serializers.ValidationError('The post with this title already exists!')       
        
        if not desc:
            raise serializers.ValidationError("The description section cannot be empty!")
            
        return attrs
    
    
class AIresponseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    chat = serializers.PrimaryKeyRelatedField(
        queryset=Chat.objects.all()
    )
    user_request = serializers.PrimaryKeyRelatedField(
        queryset=UserRequest.objects.all()
    )
    
    class Meta:
        model = AIresponse
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
        

class UserRequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    chat = serializers.PrimaryKeyRelatedField(
        queryset=Chat.objects.all()
    )
    responses = AIresponseSerializer(many=True, read_only=True)
    image = serializers.ImageField(required = False)
    
    class Meta:
        model = UserRequest
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
        

class ChatSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    
    requests = UserRequestSerializer(source='user_requests', many=True, read_only=True)
    
    responses = AIresponseSerializer(source='responces', many=True, read_only=True)
    
    class Meta:
        model = Chat
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
        
    def validate_name(self, name):
        name = name.lower().strip()
        
        if not name:
            raise serializers.ValidationError("Chat name cannot be empty")
        
        return name
    
    def validate(self, attrs):
        name = attrs.get('name').lower().strip()
        
        if self.instance:
            qs = Chat.objects.filter(name = name).exclude(pk=self.instance.pk)
        else:
            qs = Chat.objects.filter(name = name)
            
        if qs.exists():
            raise serializers.ValidationError("The chat with this name already exists!")
        
        return attrs
        


    
    