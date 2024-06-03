from django.db import models
from django.contrib.auth import get_user_model
#creating unique id for posts...
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank = True)
    profileimg = models.ImageField(upload_to='profile_images', default='default_profile_image.png')
    location = models.CharField(max_length=100, blank = True)
    last_seen = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user =models.CharField(max_length=100)
    image =models.ImageField(upload_to='post_images')
    caption =models.TextField()
    created_at =models.DateTimeField(default=datetime.now)
    no_of_likes =models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
    def delete_post(self):
        self.delete()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.user.username} - {self.text}'

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length= 100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user