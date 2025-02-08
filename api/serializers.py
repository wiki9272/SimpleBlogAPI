from rest_framework import serializers
from .models import Post, Comment, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'comments']

