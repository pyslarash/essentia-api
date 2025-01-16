from functions.generic_audio_endpoint import generic_audio_endpoint
from api.music_cultures.discogs_spotify import discogs_spotify_music_cultures
from api.music_cultures.jamendo_spotify import jamendo_spotify_music_cultures

def discogs_music_cultures_endpoint():
    """
    Classify genres for the given audio file and return results mapped to music cultures in JSON format.
    """
    return generic_audio_endpoint(discogs_spotify_music_cultures, "music_cultures")

def jamendo_music_cultures_endpoint():
    """
    Classify genres for the given audio file and return results mapped to music cultures in JSON format.
    """
    return generic_audio_endpoint(jamendo_spotify_music_cultures, "music_cultures")