from django.db import models
from django.contrib.auth.models import User
from .constants import CATEGORY_CHOICES
from django.utils import timezone

class New(models.Model):
    categories = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news/media/uploads', blank=True, null=True)
    description = models.TextField() 
    publishing_time = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new = models.ForeignKey(New, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(5)])
    date_rated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.new.title} - {self.rating}"
