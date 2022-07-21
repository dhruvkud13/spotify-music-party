from django.db import models
import string
import random

# for random code generation
def generate_unique_code():
    length = 10

    while True:
        code = ''.join(random.choices(string.ascii_lowercase, k=length))
        # to check if code is unique
        if Room.objects.filter(code=code).count() == 0:
            break

    return code

# Create your models here.
class Room(models.Model):
    code = models.CharField(max_length=10,default=generate_unique_code)
    host = models.CharField(max_length=50,unique=True)
    guest_can_pause = models.BooleanField(null=False,default=False)
    votes_to_skip = models.IntegerField(null=False,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    current_song = models.CharField(max_length=50,default="")
    # current song to keep track of votes for which song

# after creating model we want to set up an api view that can return
# all rooms that are currently in the database
# so we create an endpoint

# host is stored using session key, for this we use sessions 
# each session has unique id 
