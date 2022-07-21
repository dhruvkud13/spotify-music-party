# serializer takes the model and translates model to json response
from requests import request
from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields=('id','code','host','guest_can_pause','votes_to_skip','created_at')

class CreateRoomSerializer(serializers.ModelSerializer):
    # we use serializer here to make sure data thats being sent is valid and corresponds with correct fields needed to create new room
    class Meta:
        model = Room
        # fields that will be sent along with post request
        fields=('guest_can_pause','votes_to_skip')

class UpdateRoomSerializer(serializers.ModelSerializer):
    # we have to pass the same code as the room code thus the code passed here will never be unique
    # and there will always be invalid error
    # thus we make this change so serializer doesnt think that we need to pass unique code
    code= serializers.CharField(validators=[])
    # because of this we dont reference code field from the model
    class Meta:
        model = Room
        # fields that will be sent along with post request
        fields=('guest_can_pause','votes_to_skip','code') 
        # now code references the new code field we created