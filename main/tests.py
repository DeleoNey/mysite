from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Post, Comment

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Старий заголовок',
            content='Тестовий контент',
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Старий заголовок')
        self.assertEqual(self.post.content, 'Тестовий контент')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertTrue(self.post.slug)

    def test_total_likes(self):
        self.assertEqual(self.post.total_likes(), 0)
        self.post.likes.add(self.user)
        self.assertEqual(self.post.total_likes(), 1)


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='commenter', password='12345')
        self.post = Post.objects.create(title='Пост для коментаря', content='Контент', author=self.user)
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='Мій коментар')

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Мій коментар')
        self.assertEqual(self.comment.author.username, 'commenter')
        self.assertEqual(self.comment.post, self.post)
