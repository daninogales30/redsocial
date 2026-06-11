from django.db import models

from users.models import User


class Post(models.Model):
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    texto = models.TextField(
        blank=True,
        max_length=200
    )

    imagen = models.ImageField(
        upload_to='posts/'
    )

    fecha_publicacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return f'{self.autor.username} - {self.id}'


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f'{self.user.username} likes {self.post.id}'


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField(
        max_length=300
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username}'
