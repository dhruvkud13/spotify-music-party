from django.urls import path
from .views import AuthURL, PauseSongView, spotify_callback, IsAuthenticated, CurrentSong, PlaySongView, SkipSongNextView

urlpatterns = [
    path('get-auth-url',AuthURL.as_view()),
    path('redirect',spotify_callback),
    path('is-authenticated',IsAuthenticated.as_view()),
    path('current-song',CurrentSong.as_view()),
    path('pause',PauseSongView.as_view()),
    path('play',PlaySongView.as_view()),
    path('skip-next',SkipSongNextView.as_view()),
    # path('skip-previous',SkipSongPreviousView.as_view())
]