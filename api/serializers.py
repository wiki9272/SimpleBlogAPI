from rest_framework import serializers
from .models import Post, Comment, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PostSerializer(serializers.ModelSerializer):
    model = Post
    fields = ['__all__']

class CommentSerializer(serializers.ModelSerializer):
    model = Comment
    fields = ['__all__']