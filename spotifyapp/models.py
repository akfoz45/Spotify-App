from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=100, unique=True, primary_key=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Track(models.Model):
    name = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=100, unique=True, primary_key=True)
    album_art_url = models.URLField(max_length=500, null=True, blank=True)
    artists = models.ManyToManyField(Artist, related_name="tracks")

    def __str__(self):
        return f"{self.name} - {self.artists.first()}"
    
class SpotifyProfile(models.Model):
    spotify_id = models.CharField(max_length=100, unique=True, primary_key=True)
    display_name = models.CharField(max_length=200, null=True, blank=True)
    top_artists = models.ManyToManyField(Artist, related_name="profiles_top_artists")
    top_tracks = models.ManyToManyField(Track, related_name="profiles_top_tracks")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or self.spotify_id
