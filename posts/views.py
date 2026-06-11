import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView

from notifications.models import Notification
from posts.models import Post, Like, Comment


class LikeToggleView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

            if post.autor != request.user:
                Notification.objects.create(
                    recipient=post.autor,
                    sender=request.user,
                    type="like",
                    post=post
                )

        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})

class CommentListView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        coments = post.comments.select_related('user')

        data = {
            'comments': [
                {
                    'user': c.user.username,
                    'text': c.text
                }
                for c in coments
            ],
        }

        return JsonResponse(data)

class CommentCreateView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        body = json.loads(request.body)
        text = body.get('text')

        comment = Comment.objects.create(
            user=request.user,
            post=post,
            text=text
        )
        print("ENTRA EN COMMENT VIEW")
        # 🔥 NOTIFICACIÓN COMMENT
        if post.autor != request.user:
            Notification.objects.create(
                recipient=post.autor,
                sender=request.user,
                type="comment",
                post=post,
                comment_id=comment.id
            )
        print("CREANDO NOTIFICACION")

        comments = post.comments.select_related('user')

        data = {
            "comments": [
                {
                    "user": c.user.username,
                    "text": c.text
                }
                for c in comments
            ]
        }

        return JsonResponse(data)


class FeedView(ListView):
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.select_related('autor').prefetch_related('likes', 'comments').order_by('-fecha_publicacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['liked_posts'] = set(
                Like.objects.filter(user=self.request.user)
                .values_list('post_id', flat=True)
            )
        else:
            context['liked_posts'] = set()

        return context