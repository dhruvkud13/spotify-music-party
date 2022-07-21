from pyexpat import model
from django.db import models
from api.models import Room

# Create your models here.
class SpotifyToken(models.Model):
    user= models.CharField(max_length=50,unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    refresh_token= models.CharField(max_length=150)
    access_token= models.CharField(max_length=150)
    expires_in= models.DateTimeField()
    token_type= models.CharField(max_length=50)

class Vote(models.Model):
    # when new song starts, we have to clear votes of previous song
    user= models.CharField(max_length=50,unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    song_id= models.CharField(max_length=50)
    room= models.ForeignKey(Room, on_delete=models.CASCADE)
    # when we have foreign key we need to pass instance of another object
    # any room we have in database we can pass one when we create a new Vote
    # and it stored reference to the room in that vote model
    # all info of room can be accessed through this