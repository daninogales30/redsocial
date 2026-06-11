from django.urls import path

from posts.views import FeedView, LikeToggleView, CommentListView, CommentCreateView

app_name = 'posts'

urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('posts/<int:post_id>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('posts/<int:post_id>/comments/', CommentListView.as_view()),
    path('posts/<int:post_id>/comments/create/', CommentCreateView.as_view()),
]
