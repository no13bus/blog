from django.db import models
from django.contrib.auth.models import User


class Posts(models.Model):
    title = models.CharField(
        max_length=200, null=False, blank=False, help_text="The title of the blog post", db_index=True
    )
    content = models.TextField(null=False, blank=False, help_text="The main content of the blog post")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the post was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the post was last updated")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        db_table = "posts"


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens")
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s token ({self.token})"
