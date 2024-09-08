from django.db import models
from django.utils import timezone

class user_register(models.Model):
    id = models.AutoField(primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.username

class Post(models.Model):
    postid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Comment(models.Model):
    commentid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    text = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)
    sentiment_score = models.FloatField(null=True, blank=True)  
    sentiment_label = models.CharField(max_length=10, null=True, blank=True) 

    class Meta:
        unique_together = ('post', 'username')  # Ensure each user can comment only once per post

    def __str__(self):
        return f'Comment by {self.username} on {self.post.title}'
