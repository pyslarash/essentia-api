from functions.generic_audio_endpoint import generic_audio_endpoint
from api.mood.acoustic import acoustic
from api.mood.aggressive import aggressive
from api.mood.electronic import electronic
from api.mood.happy import happy
from api.mood.jamendo_mood_spotify import jamendo_mood_spotify
from api.mood.jamendo_mood_theme import jamendo_mood_theme
from api.mood.mirex import mirex
from api.mood.party import party
from api.mood.relaxed import relaxed
from api.mood.sad import sad

def acoustic_endpoint():
    return generic_audio_endpoint(acoustic, "acoustic")

def aggressive_endpoint():
    return generic_audio_endpoint(aggressive, "aggressive")

def electronic_endpoint():
    return generic_audio_endpoint(electronic, "electronic")

def happy_endpoint():
    return generic_audio_endpoint(happy, "happy")

def jamendo_mood_spotify_endpoint():
    return generic_audio_endpoint(jamendo_mood_spotify, "mood_spotify")

def jamendo_mood_theme_endpoint():
    return generic_audio_endpoint(jamendo_mood_theme, "jamendo_mood_theme")

def mirex_endpoint():
    return generic_audio_endpoint(mirex, "mirex")

def party_endpoint():
    return generic_audio_endpoint(party, "party")

def relaxed_endpoint():
    return generic_audio_endpoint(relaxed, "relaxed")

def sad_endpoint():
    return generic_audio_endpoint(sad, "sad")