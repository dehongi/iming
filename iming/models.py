from django.db import models
from django.conf import settings

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        if self.is_private:
            return f"Private message from {self.sender} to {self.recipient}"
        return f"Message from {self.sender}"
