from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="user_followers")
    following = models.ManyToManyField("self", symmetrical=False, related_name="user_following")

    def serialize(self):
        return{
            "username": self.username,
            "followers": list(self.followers.all()),
            "following": list(self.following.all()),
        }

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "content" : self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
        
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_liked")
    
    def serialize(self):
        return {
            "user": self.user.username,
            "post": self.post.id,
        }