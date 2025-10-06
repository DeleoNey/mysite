from django.db import models
from django.urls import reverse
# from django.utils.text import slugify
from pytils.translit import slugify
from django.contrib.auth.models import User


class Profile(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatars/default_avatar/default.jpg', upload_to='avatars/',
                               blank=True,
                               null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.username} Profile"


    def get_absolute_url(self):
        return reverse("main:profile-detail", args=[self.id, self.slug])


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True)
    slug = models.SlugField(unique=True, blank=True)

    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and Post.objects.get(pk=self.pk).title != self.title):
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("main:post-detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


    def __str__(self):
        return f"Коментар від {self.author.username} {self.post.title}"