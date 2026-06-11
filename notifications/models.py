from django.conf import settings
from django.db import models




class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("like", "Like"),
        ("comment", "Comment"),
        ("follow", "Follow"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    comment_id = models.IntegerField(null=True, blank=True)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender} -> {self.recipient} ({self.type})"
