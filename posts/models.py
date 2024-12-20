from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Post(models.Model):
    image = models.ImageField(upload_to="images/", blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")

    like = models.ManyToManyField(to=User, related_name="like_user", blank=True)

    def __str__(self):
        return self.content[:10]


class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return self.content[:10]
