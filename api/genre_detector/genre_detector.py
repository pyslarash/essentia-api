from functions.generic_audio_endpoint import generic_audio_endpoint
from api.genre_detector.discogs import discogs
from api.genre_detector.discogs_routenote import discogs_routenote
from api.genre_detector.discogs_spotify import discogs_spotify
from api.genre_detector.jamendo import jamendo
from api.genre_detector.jamendo_routenote import jamendo_routenote
from api.genre_detector.jamendo_spotify import jamendo_spotify
from functions.save_file_to_temp import save_file_to_temp

def discogs_endpoint():
    """
    Classify genres for the given audio file and return Discogs results in JSON format.
    """
    return generic_audio_endpoint(discogs, "genres")

def discogs_routenote_endpoint():
    """
    Classify genres for the given audio file and return results mapped to RouteNote genres in JSON format.
    """
    return generic_audio_endpoint(discogs_routenote, "routenote_genres")
    
def discogs_spotify_endpoint():
    """
    Classify genres for the given audio file and return results mapped to Spotify genres in JSON format.
    """
    return generic_audio_endpoint(discogs_spotify, "spotify_genres")
    

def jamendo_endpoint():
    """
    Endpoint for classifying genres using the Jamendo classifier.
    """
    return generic_audio_endpoint(jamendo, "genres")

def jamendo_routenote_endpoint():
    """
    Endpoint for classifying genres using the Jamendo classifier and mapping to RouteNote.
    """
    return generic_audio_endpoint(jamendo_routenote, "routenote_genres")

def jamendo_spotify_endpoint():
    """
    Endpoint for classifying genres using the Jamendo classifier and mapping to Spotify.
    """
    return generic_audio_endpoint(jamendo_spotify, "spotify_genres")
