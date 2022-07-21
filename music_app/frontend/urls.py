
from django.urls import path
from .views import index

app_name='frontend'
# django needs to know this urls.py file belongs to the frontend app

urlpatterns = [
    path('',index,name=''),
    path('join',index),
    path('create',index),
    path('room/<str:roomCode>',index)
]