from functions.generic_audio_endpoint import generic_audio_endpoint
from api.song_styles.discogs_spotify import discogs_spotify_song_styles
from api.song_styles.jamendo_spotify import jamendo_spotify_song_styles

def discogs_song_styles_endpoint():
    """
    Classify genres for the given audio file and return results mapped to music cultures in JSON format.
    """
    return generic_audio_endpoint(discogs_spotify_song_styles, "music_styles")

def jamendo_song_styles_endpoint():
    """
    Classify genres for the given audio file and return results mapped to music cultures in JSON format.
    """
    return generic_audio_endpoint(jamendo_spotify_song_styles, "music_styles")