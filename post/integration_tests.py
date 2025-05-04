from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from django.http import Http404
from .models import Posts
from .schemas import PostCreate, PostUpdate
from . import services


class PostServicesIntegrationTest(TestCase):
    """Integration tests for Post services with database operations"""

    def setUp(self):
        """Create test data"""
        # Create multiple posts for testing
        self.test_posts = []
        for i in range(3):
            post = Posts.objects.create(title=f"Test Post {i}", content=f"Test Content {i}")
            self.test_posts.append(post)

        # Store the first post for single post tests
        self.test_post = self.test_posts[0]

    def test_list_posts(self):
        """Test listing all posts from database"""
        posts = services.list_posts()

        # Should return all posts (3 posts)
        self.assertEqual(len(posts), 3)

        # Verify the posts are ordered by created_at
        self.assertTrue(all(posts[i].created_at >= posts[i + 1].created_at for i in range(len(posts) - 1)))

    def test_get_post(self):
        """Test retrieving a single post from database"""
        # Test getting existing post
        post = services.get_post(self.test_post.id)
        self.assertEqual(post.id, self.test_post.id)
        self.assertEqual(post.title, self.test_post.title)
        self.assertEqual(post.content, self.test_post.content)

        # Test getting non-existent post
        with self.assertRaises(Http404):
            services.get_post(999)

    def test_create_post(self):
        """Test creating a new post in database"""
        post_data = PostCreate(title="New Post", content="New Content")

        # Create new post
        new_post = services.create_post(post_data)

        # Verify post was created in database
        db_post = Posts.objects.get(id=new_post.id)
        self.assertEqual(db_post.title, post_data.title)
        self.assertEqual(db_post.content, post_data.content)

    def test_update_post(self):
        """Test updating an existing post in database"""
        original_updated_at = self.test_post.updated_at

        # Update only title
        update_data = PostUpdate(title="Updated Title")
        services.update_post(self.test_post.id, update_data)

        # Refresh from database
        self.test_post.refresh_from_db()

        # Verify changes
        self.assertEqual(self.test_post.title, "Updated Title")
        self.assertEqual(self.test_post.content, "Test Content 0")  # Original content
        self.assertGreater(self.test_post.updated_at, original_updated_at)

        # Update only content
        update_data = PostUpdate(content="Updated Content")
        services.update_post(self.test_post.id, update_data)

        # Refresh from database
        self.test_post.refresh_from_db()

        # Verify changes
        self.assertEqual(self.test_post.title, "Updated Title")  # Unchanged
        self.assertEqual(self.test_post.content, "Updated Content")

        # Update both fields
        update_data = PostUpdate(title="Final Title", content="Final Content")
        services.update_post(self.test_post.id, update_data)

        # Refresh from database
        self.test_post.refresh_from_db()

        # Verify changes
        self.assertEqual(self.test_post.title, "Final Title")
        self.assertEqual(self.test_post.content, "Final Content")

    def test_delete_post(self):
        """Test deleting a post from database"""
        post_id = self.test_post.id

        # Delete the post
        services.delete_post(post_id)

        # Verify post no longer exists in database
        self.assertFalse(Posts.objects.filter(id=post_id).exists())

        # Try to delete non-existent post
        with self.assertRaises(Http404):
            services.delete_post(999)
