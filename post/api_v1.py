from typing import List
from ninja import NinjaAPI, Router
from ninja.responses import Response
from .schemas import PostCreate, PostOut, PostUpdate, TokenRequest, TokenResponse
from django.http import HttpRequest
from . import services

router = Router(tags=["Posts"])


@router.get("/posts", response=List[PostOut], description="Get all posts.", tags=["posts"])
def list_posts(request: HttpRequest):
    return services.list_posts()


@router.get("/posts/{post_id}", response=PostOut, description="Get a single post by ID.", tags=["posts"])
def get_post(request: HttpRequest, post_id: int):
    return services.get_post(post_id)


@router.post("/posts", response={201: PostOut}, description="Create a new post.", tags=["posts"])
def create_post(request: HttpRequest, data: PostCreate):
    return services.create_post(data)


@router.put("/posts/{post_id}", response=PostOut, description="Update an existing post.", tags=["posts"])
def update_post(request: HttpRequest, post_id: int, data: PostUpdate):
    return services.update_post(post_id, data)


@router.delete("/posts/{post_id}", response={204: None}, description="Delete a post.", tags=["posts"])
def delete_post(request: HttpRequest, post_id: int):
    services.delete_post(post_id)
    return 204, None


@router.post("/auth/token", response=TokenResponse, description="Get authentication token.", tags=["auth"], auth=None)
def get_token(request: HttpRequest, data: TokenRequest):
    token = services.generate_token(data.username, data.password)
    return {"token": token}
