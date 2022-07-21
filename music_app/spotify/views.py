from multiprocessing.spawn import prepare
from django.shortcuts import redirect, render
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request,post, request
from rest_framework import status
from rest_framework.response import Response
from .util import is_spotify_authenticated, update_or_create_user_tokens, execute_spotify_api_request, pause_song, play_song, skip_song_next, skip_song_previous
from django.shortcuts import redirect
from api.models import Room
from .models import Vote

# Create your views here.
# authentication/request access view
class AuthURL(APIView):
    def get(self,request,format=None):
        # we want this info
        scopes='user-read-playback-state user-modify-playback-state user-read-currently-playing'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            # sends code back that allows us to authenticate user
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url
        # want the frontend to get this url here and send it from there
        return Response({'url':url},status=status.HTTP_200_OK)

# after authorization access, we need to send another req and get access and refresh tokens
# this is what our callback does
# when we pass the redirect uri after ths is done, it sends the info to the redirect uri

# after sending req to this url it returns info to callback func

def spotify_callback(request,format=None):
    # get pieces of info from request needed
    code= request.GET.get('code')
    error= request.GET.get('error')

    # once we get the info we send req back to spotify acc service for the tokens
    response=post('https://accounts.spotify.com/api/token',data={
        'grant_type':'authorization_code',
        'code':code,
        'redirect_uri':REDIRECT_URI,
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET
    }).json()

    # we look at this response and get the tokens
    access_token=response.get('access_token')
    token_type=response.get('token_type')
    refresh_token=response.get('refresh_token')
    expires_in=response.get('expires_in')
    error=response.get('error') 
    # now we have to store these tokens
    # there are multiple users so we create a database
    # we associate users session data with the access token
    # we need to store access tokens for hosts

    if not request.session.exists(request.session.session_key):
            request.session.create()
    update_or_create_user_tokens(request.session.session_key,access_token,token_type,expires_in,refresh_token)
    # we want to redirect to the host page
    return redirect('frontend:')
    # to redirect to page inside of frontend we use colon

# from frotnend we call AuthURL, we then take the url returned to us and redirect to that page,
# then once user is done authorising us, url will redirect to spotify calllback function
# then we send req for tokens, store them and redirect back to original app


# view which tells us if we are authenticated
class IsAuthenticated(APIView):
    def get(self,request,format=None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        # we call is_spotify_authenticated func and return json response to tell if authenticated or not
        is_authenticated=is_spotify_authenticated(self.request.session.session_key)
        return Response({'is_authenticated':is_authenticated},status=status.HTTP_200_OK)


# view to return info about current song
class CurrentSong(APIView):
    def get(self,request,format=None):
        room_code= self.request.session.get('room_code')
        # we have to check if person asking info about song is host or not
        # we need to use the host info to get info about the song
        room=Room.objects.filter(code=room_code)
        if room.exists():
            room=room[0]
        else:
            return Response({},status=status.HTTP_404_NOT_FOUND)
        host=room.host
        # now we can get token info related to host
        endpoint="player/currently-playing"
        # req has to be sent to spotify along with token
        response= execute_spotify_api_request(host, endpoint)
        # we see what is in the response
        # print(response)
        # now we get all the song data
        # item is the key we are looking for it has all info about the song
        if 'error' in response or 'item' not in response:
            return Response({},status=status.HTTP_204_NO_CONTENT)
        # so now we have song then
        item= response.get('item')
        duration= item.get('duration_ms')
        progress= response.get('progress_ms')
        album_cover= item.get('album').get('images')[0].get('url')
        is_playing= response.get('is_playing')
        song_id= item.get('id')
        # if multiple artists, artist tag will have multiple artists in it
        artists_string=""
        for i, artist in enumerate(item.get('artists')):
            if i>0:
                # for other artists except first one
                artists_string+=", "
            name= artist.get('name')
            artists_string+=name
        # we send back no of votes for current song in the room
        # votes_previous=len(Vote.objects.filter(room=room,song_id=song_id))
        votes_next=len(Vote.objects.filter(room=room,song_id=song_id))
        song={
            'title': item.get('name'),
            'artist': artists_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            # 'votes_previous':votes_previous,
            'votes_next':votes_next,
            'votes_required':room.votes_to_skip,
            'id':song_id
        }

        self.update_room_song(room,song_id)

        return Response(song,status=status.HTTP_200_OK)

    def update_room_song(self,room,song_id):
        current_song= room.current_song

        if current_song != song_id:
            room.current_song=song_id
            room.save(update_fields=['current_song'])
            # to save room with updated current song
            # now after updating any votes in this room will be invalid coz 
            # they were valid for previous song so we need to delete these votes
            votes= Vote.objects.filter(room=room).delete()


class PauseSongView(APIView):
    def put(self,response,format=None):
        # req we send to spotify api is put req so we mirror
        # check if user has permission to pause play
        room_code= self.request.session.get('room_code')
        room=Room.objects.filter(code=room_code)[0]
        # now we check if guest can play/pause or if user is host
        if self.request.session.session_key==room.host or room.guest_can_pause:
            # print(self.request.session.session_key)
            # print(room.host)
            pause_song(room.host)
            return Response({},status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_403_FORBIDDEN)

class PlaySongView(APIView):
    def put(self,response,format=None):
        # req we send to spotify api is put req so we mirror
        # check if user has permission to pause play
        room_code= self.request.session.get('room_code')
        room=Room.objects.filter(code=room_code)[0]
        # now we check if guest can play/pause or if user is host
        if self.request.session.session_key==room.host or room.guest_can_pause:
            play_song(room.host)
            return Response({},status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_403_FORBIDDEN)

class SkipSongNextView(APIView):
    # post coz we are adding new vote
    def post(self,request,format=None):
        room_code = self.request.session.get('room_code')
        room=Room.objects.filter(code=room_code)[0]
        votes_next=Vote.objects.filter(room=room, song_id= room.current_song)
        votes_needed_next= room.votes_to_skip

        if self.request.session.session_key== room.host or len(votes_next)+1 >= votes_needed_next:
            votes_next.delete()
            skip_song_next(room.host)
        else:
            vote= Vote(user=self.request.session.session_key,room=room,song_id=room.current_song)
            vote.save()
        return Response({},status=status.HTTP_204_NO_CONTENT)

# class SkipSongPreviousView(APIView):
#     # post coz we are adding new vote
#     def post(self,request,format=None):
#         room_code = self.request.session.get('room_code')
#         room=Room.objects.filter(code=room_code)[0]
#         votes_previous=Vote.objects.filter(room=room, song_id= room.current_song)
#         # song_id param will ensure we grab only new votes
#         votes_needed_previous= room.votes_to_skip

#         if self.request.session.session_key== room.host or len(votes_previous)+1 >= votes_needed_previous:
#         # plus 1 coz current user plus votes of others so far
#         # if we skip song we should clear all votes we just had
#         # so we clear all votes and then song is skipped
#             votes_previous.delete()
#             skip_song_previous(room.host)
#         else:
#             vote= Vote(user=self.request.session.session_key,room=room,song_id=room.current_song)
#             vote.save()

#             # we create a model vote to store user votes
#             # if someone is voting and they are not host we create a new vote and add that
#         return Response({},status=status.HTTP_204_NO_CONTENT)