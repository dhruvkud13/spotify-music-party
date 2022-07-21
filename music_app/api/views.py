from cgitb import lookup
import code
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse


# Create your views here.
# we write api view which lets us view list of all diff rooms
class RoomView(generics.ListAPIView):
    queryset=Room.objects.all()
    serializer_class=RoomSerializer

class GetRoom(APIView):
    serializer_class=RoomSerializer
    lookup_url_kwarg='code'

    def get(self,request,format=None):
        code= request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room= Room.objects.filter(code=code)
            if len(room)>0:
                data= RoomSerializer(room[0]).data
                data['is_host']= self.request.session.session_key == room[0].host
                return Response(data, status= status.HTTP_200_OK)
            return Response({'Room not found':'Invalid Room Code'}, status= status.HTTP_404_NOT_FOUND)
        return Response ({'Bad Request':'Code Parameter not found in request'}, status= status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    lookup_url_kwarg='code'
    def post(self,request,format=None):
        # check if user has active session
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code= request.data.get(self.lookup_url_kwarg)
        if code != None:
            roomResult = Room.objects.filter(code=code)
            if len(roomResult)>0:
                room = roomResult[0]
                # make a note at the backend that this user is in the room
                # with this if user leaves site by mistake he can rejoin without entering code
                # creating object room_code to store code in the user session
                self.request.session['room_code']= code
                return Response({'message':'Room Joined!!'},status=status.HTTP_200_OK)
            return Response({'Bad Request':'Invalid Room Code'}, status= status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request':'Code Parameter not found in request'}, status= status.HTTP_400_BAD_REQUEST)

class UserInRoomView(APIView):
    # inherited from api view
    def get(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data={
            'code':self.request.session.get('room_code'),
            # getting room code info from the session
        }
        # json response takes python dictionary and serializes it using json serializer and 
        # sends the info back with the request
        return JsonResponse(data,status=status.HTTP_200_OK)

class LeaveRoomView(APIView):
    # we are changing info on server
    # we remove the room code from users session thats why post req
    def post(self,request,format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id= self.request.session.session_key
            roomResult= Room.objects.filter(host=host_id)
            if len(roomResult)>0:
                room= roomResult[0]
                room.delete()
        return Response({'message':'Room Deleted'},status=status.HTTP_200_OK)


class CreateRoomView(APIView):
    serializer_class=CreateRoomSerializer
    def post(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause= serializer.data.get('guest_can_pause')
            votes_to_skip= serializer.data.get('votes_to_skip')
            host= self.request.session.session_key
        # if room already exists then we update room with same room code
            queryset= Room.objects.filter(host=host)
            if queryset.exists():
                room= queryset[0]
                room.guest_can_pause= guest_can_pause
                room.votes_to_skip= votes_to_skip
                room.save(update_fields=['guest_can_pause','votes_to_skip'])
                self.request.session['room_code']= room.code
            else:
                room= Room(host=host,guest_can_pause=guest_can_pause,votes_to_skip=votes_to_skip)
                room.save()
                self.request.session['room_code']= room.code
            return Response(RoomSerializer(room).data,status=status.HTTP_201_CREATED)

class UpdateRoomView(APIView):
    # we need information for updating so we use serializer class
    serializer_class= UpdateRoomSerializer
    def patch(self,request,format=None):
        # patch method is used to update
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer= self.serializer_class(data=request.data)
        # passing data to serializer to check if its valid
        if serializer.is_valid():
            guest_can_pause=serializer.data.get('guest_can_pause')
            votes_to_skip=serializer.data.get('votes_to_skip')
            code= serializer.data.get('code')
            # now we find room which has this data
            queryset= Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({'Bad Request':'Invalid Room Code'}, status= status.HTTP_404_NOT_FOUND)
            room= queryset[0]
            # we need to make sure person updating is owner and match the session keys
            user_id= self.request.session.session_key
            if room.host != user_id:
                return Response({'Bad Request':'You are not the owner of this room'}, status= status.HTTP_403_FORBIDDEN)
            room.guest_can_pause= guest_can_pause
            room.votes_to_skip= votes_to_skip
            room.save(update_fields=['guest_can_pause','votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({'Bad Request':'Invalid Data'},status=status.HTTP_400_BAD_REQUEST)
