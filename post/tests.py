from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.http import Http404
from datetime import datetime
from pydantic import ValidationError

from .services import list_posts, get_post, create_post, update_post, delete_post
from .models import Posts
from .schemas import PostCreate, PostUpdate, PostOut


class PostServicesUnitTest(TestCase):
    """Unit tests for Post services layer"""

    def setUp(self):
        """Set up test data and mocks"""
        # Create a sample post data that matches the PostOut schema
        self.sample_post_data = {
            "id": 1,
            "title": "Test Post",
            "content": "Test Content",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        # Create a sample post instance
        self.sample_post = MagicMock(spec=Posts)
        for key, value in self.sample_post_data.items():
            setattr(self.sample_post, key, value)

    @patch("post.services.Posts.objects")
    def test_list_posts(self, mock_objects):
        """Test listing all posts

        Should:
        1. Return all posts from the database
        2. Return empty list when no posts exist
        """
        # Setup mock to return a list of posts
        mock_objects.all.return_value = [self.sample_post]

        # Test with existing posts
        result = list_posts()
        mock_objects.all.assert_called_once()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.sample_post_data["id"])
        self.assertEqual(result[0].title, self.sample_post_data["title"])

        # Test with empty list
        mock_objects.all.return_value = []
        result = list_posts()
        self.assertEqual(len(result), 0)

    @patch("post.services.get_object_or_404")
    def test_get_post(self, mock_get_object):
        """Test retrieving a single post

        Should:
        1. Return the post if it exists
        2. Raise Http404 if post doesn't exist
        """
        # Setup mock to return a post
        mock_get_object.return_value = self.sample_post

        # Test retrieving existing post
        result = get_post(1)
        mock_get_object.assert_called_with(Posts, pk=1)
        self.assertEqual(result.id, self.sample_post_data["id"])
        self.assertEqual(result.title, self.sample_post_data["title"])

        # Test retrieving non-existent post
        mock_get_object.side_effect = Http404
        with self.assertRaises(Http404):
            get_post(999)

    def test_create_post_validation(self):
        """Test post creation validation

        Should:
        1. Validate title length (1-200 characters)
        2. Validate content length (1-1000 characters)
        3. Validate required fields
        """
        # Test empty title
        with self.assertRaises(ValidationError) as context:
            PostCreate(title="", content="Test Content")
        self.assertIn("title", str(context.exception))

        # Test title too long (> 200 characters)
        with self.assertRaises(ValidationError) as context:
            PostCreate(title="A" * 201, content="Test Content")
        self.assertIn("title", str(context.exception))

        # Test empty content
        with self.assertRaises(ValidationError) as context:
            PostCreate(title="Test", content="")
        self.assertIn("content", str(context.exception))

        # Test content too long (> 1000 characters)
        with self.assertRaises(ValidationError) as context:
            PostCreate(title="Test", content="A" * 1001)
        self.assertIn("content", str(context.exception))

        # Test missing title
        with self.assertRaises(ValidationError) as context:
            PostCreate(content="Test Content")
        self.assertIn("title", str(context.exception))

        # Test missing content
        with self.assertRaises(ValidationError) as context:
            PostCreate(title="Test")
        self.assertIn("content", str(context.exception))

        # Test valid title lengths
        try:
            # Test minimum length (1 character)
            PostCreate(title="A", content="Test Content")
            # Test maximum length (200 characters)
            PostCreate(title="A" * 200, content="Test Content")
        except ValidationError:
            self.fail("Valid title lengths should not raise ValidationError")

    @patch("post.services.Posts.objects")
    def test_create_post(self, mock_objects):
        """Test creating a new post

        Should:
        1. Create a new post with valid data
        2. Return the created post
        """
        # Setup mock to return a new post
        mock_objects.create.return_value = self.sample_post

        # Create post data with valid lengths
        post_data = PostCreate(
            title="Test Post", content="Test Content"  # Valid: within 200 chars  # Valid: within 1000 chars
        )

        # Test post creation
        result = create_post(post_data)
        mock_objects.create.assert_called_once_with(**post_data.dict())
        self.assertEqual(result.title, self.sample_post_data["title"])
        self.assertEqual(result.content, self.sample_post_data["content"])

    def test_update_post_validation(self):
        """Test post update validation

        Should:
        1. Validate title length (1-200 characters) when provided
        2. Validate content length (1-1000 characters) when provided
        3. Validate at least one field is provided
        4. Allow partial updates
        """
        # Test empty title
        with self.assertRaises(ValidationError) as context:
            PostUpdate(title="")
        self.assertIn("title", str(context.exception))

        # Test title too long (> 200 characters)
        with self.assertRaises(ValidationError) as context:
            PostUpdate(title="A" * 201)
        self.assertIn("title", str(context.exception))

        # Test empty content
        with self.assertRaises(ValidationError) as context:
            PostUpdate(content="")
        self.assertIn("content", str(context.exception))

        # Test content too long (> 1000 characters)
        with self.assertRaises(ValidationError) as context:
            PostUpdate(content="A" * 1001)
        self.assertIn("content", str(context.exception))

        # Test no fields provided
        with self.assertRaises(ValidationError) as context:
            PostUpdate()
        self.assertIn("At least one of 'title' or 'content' must be provided", str(context.exception))

        # Test valid updates
        try:
            # Test minimum title length
            PostUpdate(title="A")
            # Test maximum title length
            PostUpdate(title="A" * 200)
            # Test normal content update
            PostUpdate(content="New Content")
            # Test both fields update
            PostUpdate(title="New Title", content="New Content")
        except ValidationError:
            self.fail("Valid updates should not raise ValidationError")

    @patch("post.services.get_object_or_404")
    def test_update_post(self, mock_get_object):
        """Test updating an existing post

        Should:
        1. Update post with new title only
        2. Update post with new content only
        3. Update post with both new title and content
        4. Raise Http404 if post doesn't exist
        """
        # Setup mock to return an existing post
        mock_get_object.return_value = self.sample_post

        # Test updating title only
        update_data = PostUpdate(title="New Title")
        result = update_post(1, update_data)
        self.assertEqual(self.sample_post.title, "New Title")
        self.sample_post.save.assert_called_once()
        self.sample_post.save.reset_mock()

        # Test updating content only
        update_data = PostUpdate(content="New Content")
        result = update_post(1, update_data)
        self.assertEqual(self.sample_post.content, "New Content")
        self.sample_post.save.assert_called_once()
        self.sample_post.save.reset_mock()

        # Test updating both title and content
        update_data = PostUpdate(title="Updated Title", content="Updated Content")
        result = update_post(1, update_data)
        self.assertEqual(self.sample_post.title, "Updated Title")
        self.assertEqual(self.sample_post.content, "Updated Content")
        self.sample_post.save.assert_called_once()

        # Test updating non-existent post
        mock_get_object.side_effect = Http404
        with self.assertRaises(Http404):
            update_post(999, update_data)

    @patch("post.services.get_object_or_404")
    def test_delete_post(self, mock_get_object):
        """Test deleting a post

        Should:
        1. Delete the post if it exists
        2. Raise Http404 if post doesn't exist
        """
        # Setup mock to return a post
        mock_get_object.return_value = self.sample_post

        # Test deleting existing post
        delete_post(1)
        mock_get_object.assert_called_with(Posts, pk=1)
        self.sample_post.delete.assert_called_once()

        # Test deleting non-existent post
        mock_get_object.side_effect = Http404
        with self.assertRaises(Http404):
            delete_post(999)
