from django.urls import path
from .views import RoomView, CreateRoomView, GetRoom, JoinRoom, UserInRoomView, LeaveRoomView, UpdateRoomView

urlpatterns = [
    path('room',RoomView.as_view()),
    path('create-room',CreateRoomView.as_view()),
    path('get-room',GetRoom.as_view()),
    path('join-room',JoinRoom.as_view()),
    path('user-in-room',UserInRoomView.as_view()),
    path('leave-room',LeaveRoomView.as_view()),
    path('update-room',UpdateRoomView.as_view())

]