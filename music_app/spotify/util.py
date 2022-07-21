from datetime import timedelta
from email import header
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from requests import Request,post,put,get
from .credentials import CLIENT_ID,CLIENT_SECRET

BASE_URL = 'https://api.spotify.com/v1/me/'

def get_user_tokens(session_id):
    user_tokens= SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

# function to store tokens
def  update_or_create_user_tokens(session_id,access_token,token_type,expires_in,refresh_token):
    # look if existing user has any tokens
    tokens= get_user_tokens(session_id)
    # 3600 seconds is life of a token
    expires_in= timezone.now()+ timedelta(seconds=expires_in)
    if tokens:
        # update tokens
        tokens.access_token= access_token
        tokens.token_type= token_type
        tokens.expires_in= expires_in
        tokens.refresh_token= refresh_token
        tokens.save(update_fields=['access_token','token_type','expires_in','refresh_token'])
    else:
        # create new tokens
        tokens= SpotifyToken(user=session_id,access_token=access_token,token_type=token_type,expires_in=expires_in,refresh_token=refresh_token)
        tokens.save()

# to check if user is currently authenticated
def is_spotify_authenticated(session_id):
    tokens= get_user_tokens(session_id)
    if tokens:
        expiry=tokens.expires_in
        if expiry<= timezone.now():
        # now we refresh tokens
            refresh_spotify_token(session_id)
        return True

    return False

# to refresh token
def refresh_spotify_token(session_id):
    refresh_token= get_user_tokens(session_id).refresh_token

    response=post('https://accounts.spotify.com/api/token',data={
        # we are sending refresh token
        'grant_type':'refresh_token',
        'refresh_token':refresh_token,
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET
    }).json()

    # we get the new access tokens
    access_token=response.get('access_token')
    token_type=response.get('token_type')
    expires_in=response.get('expires_in')
    # refresh_token=response.get('refresh_token')
    # we dont need last line as refresh token stays the same 

    update_or_create_user_tokens(session_id,access_token,token_type,expires_in,refresh_token)

def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    # post_ and put_ to handle diff types of requests, they mirror post and put functions
    tokens= get_user_tokens(session_id)
    headers={'Content-Type':'application/json','Authorization':'Bearer ' + tokens.access_token}
    # print(session_id)
    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        # print(BASE_URL+endpoint)
        # print(tokens.access_token)
        # print(headers)
        # print(BASE_URL+endpoint, headers=headers)
        put(BASE_URL+endpoint, headers=headers)
        
    # if no put or post, then get request
    response= get(BASE_URL+ endpoint , {}, headers=headers)
    try:
        return response.json()
    except:
        return{'Error':'Request Issue'}
# with this function we can send req to any spotify endpoint

def play_song(session_id):
    return execute_spotify_api_request(session_id,'player/play',put_=True)
    # player/play is endpoint to play song

def pause_song(session_id):
    # print(session_id)
    return execute_spotify_api_request(session_id,'player/pause',put_=True)
    # player/pause is endpoint to play song

def skip_song_next(session_id):
    return execute_spotify_api_request(session_id,'player/next',post_=True)
    # player/next is endpoint to skip song

def skip_song_previous(session_id):
    return execute_spotify_api_request(session_id,'player/previous',post_=True)
    # player/previous is endpoint to go to previous song