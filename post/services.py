from typing import List
from .models import Posts, UserToken
from .schemas import PostCreate, PostOut, PostUpdate
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from ninja.errors import HttpError
import secrets


def list_posts() -> List[PostOut]:
    return Posts.objects.all()


def get_post(post_id: int) -> PostOut:
    return get_object_or_404(Posts, pk=post_id)


def create_post(data: PostCreate) -> PostOut:
    return Posts.objects.create(**data.dict())


def update_post(post_id: int, data: PostUpdate) -> PostOut:
    post = get_object_or_404(Posts, pk=post_id)
    if data.title:
        post.title = data.title
    if data.content:
        post.content = data.content
    post.save()
    return post


def delete_post(post_id: int) -> None:
    post = get_object_or_404(Posts, pk=post_id)
    post.delete()


def generate_token(username: str, password: str) -> str:
    user = authenticate(username=username, password=password)
    if not user:
        raise HttpError(401, "Invalid credentials")

    # Generate a secure random token
    token = secrets.token_urlsafe(32)

    # Create token with 24 hour expiry
    expires_at = timezone.now() + timedelta(hours=24)
    UserToken.objects.create(user=user, token=token, expires_at=expires_at)

    return token
