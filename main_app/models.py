from unittest.util import _MAX_LENGTH
from django.db import models
import time
from django.contrib.auth.models import User


class Artists(models.Model):
# Create your models here.
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    bio = models.TextField(max_length=500)
    verified_artist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Here is our new column
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        
        
# below Artist Model

class Song(models.Model):

    title = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    artist = models.ForeignKey(
        Artists, on_delete=models.CASCADE, related_name="songs")

    def __str__(self):
        return self.title

    # Here we define the method to look at the length property and convert it
    def get_length(self):
        return time.strftime("%-M:%S", time.gmtime(self.length))


class Playlist(models.Model):

    title = models.CharField(max_length=150)
    song = models.ManyToManyField(Song)

    def __str__(self):
        return self.title
