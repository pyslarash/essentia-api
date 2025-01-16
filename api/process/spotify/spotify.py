from functions.generic_audio_endpoint import generic_audio_endpoint
from api.process.spotify.discogs_pitch import discogs_spotify_pitch
from api.process.spotify.jamendo_pitch import jamendo_spotify_pitch

def discogs_spotify_pitch_endpoint():
    return generic_audio_endpoint(discogs_spotify_pitch, "spotify_pith_info")

def jamendo_spotify_pitch_endpoint():
    return generic_audio_endpoint(jamendo_spotify_pitch, "spotify_pith_info")