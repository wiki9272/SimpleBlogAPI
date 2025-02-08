from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment, User
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated

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
                    "id": user.id,
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
    def get(self, request):
        return Response({'msg':'get request working'}, status=200)
    
class CommentView(APIView):
    def get(self, request):
        return Response({'msg':'get request working'}, status=200)