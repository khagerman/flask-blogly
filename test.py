from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///user_test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserTesting(TestCase):
    """Tests for Users"""

    def setUp(self):
        """Add sample user"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Test", last_name="Person")
        db.session.add(user)
        db.session.commit()

        self.id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            """test users page loading"""
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test", html)

    def test_show_user(self):
        with app.test_client() as client:
            """test user profile loading"""
            resp = client.get(f"/users/{self.id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Test Person</h1>", html)

    def test_add_user(self):
        with app.test_client() as client:
            """test creation of new user and redirect"""
            d = {
                "first_name": "George",
                "last_name": "The Monkey",
                "image_url": "https://media.npr.org/assets/img/2016/09/27/curious-george-2_wide-b411b6d315890c7058ec85f42771142c9c15bc34.jpg",
            }
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("George The Monkey", html)


class PostTesting(TestCase):
    """Tests for posts"""

    def setUp(self):
        """Add sample user"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Test", last_name="Person")
        db.session.add(user)
        db.session.commit()
        self.id = user.id
        self.user = user
        post = Post(title="Test Post", content="Test test test!", user_id=f"{self.id}")
        db.session.add(post)
        db.session.commit()
        self.post = post
        self.post.id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_add_tag(self):
        with app.test_client() as client:
            """Test adding a new tag"""
            d = {"name": "funny"}
            resp = client.post(f"/tags/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("funny", html)

    def test_add_post(self):
        with app.test_client() as client:
            """test creation of new post and redirect"""
            d = {
                "title": "well hello there",
                "content": "I am a test person. I test things. ",
                "tags": 1,
            }
            resp = client.post(
                f"/users/{self.id}/posts/new", data=d, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("well hello there", html)

    def test_edit_post(self):
        with app.test_client() as client:
            """test editing of new post"""
            d = {
                "title": "well bye",
                "content": "I am  not a test person. I do not test things.",
            }
            resp = client.post(
                f"/posts/{self.post.id}/edit", data=d, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("well bye", html)

            self.assertNotIn("Test Post", html)
