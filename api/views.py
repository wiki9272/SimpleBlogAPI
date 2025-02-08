from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # Number of posts per page
    page_size_query_param = 'page_size'
    max_page_size = 100

#function to get token pair
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#for user login
class LoginView(APIView):
    def post(self, request):
        #Authenticate the user and return a JWT token.
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Generate JWT tokens
            token = get_tokens_for_user(user)
            return Response({
                "token":token,
                    "user": {
                    "email": user.email,
                    "name": user.name,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

#for user signup
class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#for user change password
class ChangePassView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({"error": "Old password and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(old_password, user.password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

class PostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        post_id = request.query_params.get('id')
        search_query = request.query_params.get('search', '')

        if post_id: 
            try:
                post = Post.objects.get(pk=post_id)
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Post.DoesNotExist:
                return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Handle search and pagination
        posts = Post.objects.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        ).order_by('-created_at')

        paginator = CustomPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        data['author'] = request.user.email 
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        post_id = request.query_params.get('id')
        if not post_id:
            return Response({"error": "Post ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(pk=post_id, author=request.user)
        except Post.DoesNotExist:
            return Response({"error": "Post not found or you don't have permission to edit this post."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        post_id = request.query_params.get('id')
        if not post_id:
            return Response({"error": "Post ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = Post.objects.get(pk=post_id, author=request.user)
        except Post.DoesNotExist:
            return Response({"error": "Post not found or you don't have permission to delete this post."}, status=status.HTTP_404_NOT_FOUND)
        
        post.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_200_OK)
    
class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        post_id = request.query_params.get('id')
        if not post_id:
            return Response({"error": "Post ID is required."}, status=status.HTTP_400_BAD_REQUEST )
        
        try:
            comments = Comment.objects.filter(post = post_id)
        except Comment.DoesNotExist:
            return Response({'error':'No comment found or no permission'}, status=404)
        serializer = CommentSerializer(instance=comments, many=True)
        return Response({'comments':serializer.data}, status= 200)
    
    def post(self, request):
        data = request.data
        post_id = data.get('post')

        if not post_id:
            return Response({"error": "Post ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(author=request.user)  # Pass `author` explicitly
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        comment_id = request.query_params.get('id')
        if not comment_id:
            return Response({"error": "Comment ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found or you don't have permission to edit this comment."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        comment_id = request.query_params.get('id')
        if not comment_id:
            return Response({"error": "Comment ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found or you don't have permission to delete this comment."}, status=status.HTTP_404_NOT_FOUND)
        
        comment.delete()
        return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)