from django.db import models

from api.accounts.models import User
from api.gallery.models import Gallery


# Create your models here.
class Post(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=120)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="post_image")
    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return self.pk


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return self.pk


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.BooleanField()
