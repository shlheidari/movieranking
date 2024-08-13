from django.db import models
from django.contrib.auth.models import User, AbstractUser

class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField()
    genre = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField()
    download_link = models.URLField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

# class CustomUser(AbstractUser):
#     security_question = models.CharField(max_length=255)
#     security_answer = models.CharField(max_length=255)
