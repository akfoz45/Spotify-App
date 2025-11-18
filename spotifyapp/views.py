from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import spotipy
import uuid
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .models import SpotifyProfile, Artist, Track
from django.utils import timezone
from datetime import timedelta


def login_view(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=request.build_absolute_uri(reverse('spotify_callback')),
        scope="user-top-read user-read-recently-played",
        show_dialog=True,
        cache_path=None
    )

    state = str(uuid.uuid4())
    request.session['spotify_auth_state'] = state

    auth_url = sp_oauth.get_authorize_url(state=state)

    return redirect(auth_url)


def callback_view(request):
    stored_state = request.session.get('spotify_auth_state', None)

    received_state = request.GET.get('state')

    if stored_state is None or received_state != stored_state:
        return HttpResponseForbidden("Error: Parameter 'State' does not match.")
    
    received_code = request.GET.get('code')

    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=request.build_absolute_uri(reverse('spotify_callback')),
        scope="user-top-read user-read-recently-played",
        show_dialog=True,
        cache_path=None
    )

    try:
        if 'spotify_auth_state' in request.session:
             del request.session['spotify_auth_state']

        token_info = sp_oauth.get_access_token(received_code, check_cache=False)
    except SpotifyException as e:
        return HttpResponse(f"An error occurred while retrieving the token: {e}")
    
    request.session['spotify_token_info'] = token_info

    return redirect('spotify_profile')


def profile_view(request):
    token_info = request.session.get('spotify_token_info', None)

    if not token_info:
        return redirect('spotify_login')
    
    try:
        sp = spotipy.Spotify(auth=token_info['access_token'])

        selected_range = request.GET.get('time_range', 'long_term') 

        if selected_range not in ['short_term', 'medium_term', 'long_term']:
            selected_range = 'long_term'
    
        user_data = sp.current_user()
        profile, created = SpotifyProfile.objects.get_or_create(
            spotify_id = user_data['id'],
            defaults={'display_name': user_data['display_name']}
        )

        should_update = (
            created or
            profile.last_updated < (timezone.now() - timedelta(hours=1)) or
            'time_range' in request.GET
        )

        if should_update:
            top_artists_data = sp.current_user_top_artists(limit=10, time_range=selected_range)
            profile.top_artists.clear()
            
            for artist_data in top_artists_data['items']:
                
                artist_image_url = artist_data['images'][0]['url'] if  artist_data['images'] else None
                
                artist, _ = Artist.objects.get_or_create(
                    spotify_id = artist_data['id'],
                    defaults={'name': artist_data['name'], 'image_url': artist_image_url}
                )
                profile.top_artists.add(artist)

            top_tracks_data = sp.current_user_top_tracks(limit=10, time_range="long_term")
            profile.top_tracks.clear()
            for track_data in top_tracks_data['items']:
                album_art = track_data['album']['images'][0]['url'] if track_data['album']['images'] else None
                track , _ = Track.objects.get_or_create(
                    spotify_id = track_data['id'],
                    defaults={
                        'name': track_data['name'], 
                        'album_art_url': album_art,
                        }
                )

                track.artists.clear()

                for artist_data in track_data['artists']:
                    artist, _ = Artist.objects.get_or_create(
                        spotify_id = artist_data['id'],
                        defaults={'name': artist_data['name']}
                    )
                    track.artists.add(artist)

                profile.top_tracks.add(track)

            profile.save()

        top_tracks = profile.top_tracks.all()
        top_artists = profile.top_artists.all()

        recent_tracks = sp.current_user_recently_played(limit=10)
    
    except SpotifyException as e:
        request.session.pop('spotify_token_info', None)
        return redirect('spotify_login')
    
    context = {
        'top_tracks': top_tracks,  
        'top_artists': top_artists, 
        'recent_tracks': recent_tracks['items'], 
        'profile': profile,
        'selected_range': selected_range,
    }

    return render(request, 'spotifyapp/profile.html', context)


def logout_view(request):
    #if 'spotify_token_info' in request.session:
        #del request.session['spotify_token_info']

    request.session.flush()

    return redirect('spotify_login')