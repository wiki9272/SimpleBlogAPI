from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import PostView, CommentView, LoginView, SignUpView, ChangePassView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('signup/', SignUpView.as_view(), name='signup_view'),
    path('change-pass/', ChangePassView.as_view(), name='change_password'),
    path('posts/', PostView.as_view(), name='post_view'),
    path('comments/', CommentView.as_view(), name='comment_view'),
]