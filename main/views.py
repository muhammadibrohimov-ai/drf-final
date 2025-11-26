from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission

from drf_spectacular.utils import extend_schema, inline_serializer


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    Post,
    Comment,
    Chat,
    UserRequest,
    AIresponse
)
from .serializers import (
    PostSerializer,
    CommentSerializer,
    ChatSerializer,
    UserRequestSerializer,
    AIresponseSerializer,
    CustomTokenObtainSerializer
)


# Create your views here.


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


@extend_schema(
    tags=['Get JWT refresh and access token'],
    summary= 'Use to get your refresh and access token (refreshh for one day while acces for five)',
)
class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
    

class HomeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]
    
    def get(self, request):
        posts = get_list_or_404(Post)
        post_serializer = PostSerializer(posts, many=True)
        chats = get_list_or_404(Chat, user__id = request.user.id)
        chat_serializer = ChatSerializer(chats, many=True)
        
        return Response([post_serializer.data, chat_serializer.data], status=status.HTTP_200_OK)   
    
    
class PersonalPostsView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]
    
    def get(self, request):
        posts = get_list_or_404(Post, user__id = request.user.id)
        post_serializer = PostSerializer(posts, many=True)
        return Response(post_serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        new_post = request.data
        post_serializer = PostSerializer(data=new_post)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response({'message': "New post has been created!", 'data': post_serializer.data}, status=status.HTTP_200_OK)
        return Response(post_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
       
    
class PersonalPostDetailView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]
    
    def update(self, request, pk, partial):
        new_data = request.data
        existence = get_object_or_404(Post, pk=pk, user__id = request.user.id)
        post_serializer = PostSerializer(data=new_data, instance=existence, partial=partial)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response({'message': 'The post has been changed!', 'data': post_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, pk):
        existence = get_object_or_404(Post, pk=pk)
        existence.views += 1
        existence.save()
        post_serializer = PostSerializer(existence)
        return Response(post_serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        return self.update(request, pk, partial=False)
        
        
    def patch(self, request, pk):
        return self.update(request, pk, partial=True)
    
    
    def delete(self, request, pk):
        existence = get_object_or_404(Post, pk=pk)
        existence.delete()
        return Response({"message": f'The post has been deleted'}) 
    
    
    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        existence = get_object_or_404(Post, pk=pk)
        existence.likes += 1
        existence.save()
        post_serializer = PostSerializer(existence)
        return Response(post_serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['POST'])
    def dislike(self, request, pk):
        existence = get_object_or_404(Post, pk=pk)
        existence.likes -= 1
        existence.save()
        post_serializer = PostSerializer(existence)
        return Response(post_serializer.data, status=status.HTTP_200_OK)
        
    
    
    

class CommentView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]
    
    
    def update(self, request, comment_pk, partial):
        new_data = request.data
        comment = Comment.objects.get(pk = comment_pk)
        comment_serializer = CommentSerializer(data=request.data, instance=comment, partiali=partial)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response({'message': 'The comment has been changed!', 'data': comment_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, comment_pk):
        return self.update(request, comment_pk, partial=False)      
    
    
    def patch(self, request, comment_pk):
        return self.update(request, comment_pk, partial=True)        


    def delete(self, request, comment_pk):
        existence = get_object_or_404(Comment, pk=comment_pk)
        existence.delete()
        return Response({"message": f'The comment has been deleted!'}) 

