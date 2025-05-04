from ninja import Schema
from pydantic import constr
from datetime import datetime
from pydantic import Field
from pydantic import model_validator


class PostCreate(Schema):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=1000)


class PostUpdate(Schema):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1, max_length=1000)

    @model_validator(mode="after")
    def check_at_least_one_field(cls, values):
        if values.title is None and values.content is None:
            raise ValueError("At least one of 'title' or 'content' must be provided.")
        return values


class PostOut(Schema):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class TokenRequest(Schema):
    username: str
    password: str


class TokenResponse(Schema):
    token: str
