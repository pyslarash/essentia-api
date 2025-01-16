from functions.generic_audio_endpoint import generic_audio_endpoint

# Import functions
from api.context.approachability import approachability
from api.context.arouseness_em import arouseness_em
from api.context.arouseness_ev import arouseness_ev
from api.context.arouseness_mm import arouseness_mm
from api.context.arouseness_mv import arouseness_mv
from api.context.audio_events import audio_events
from api.context.danceability import danceability
from api.context.engagement import engagement
from api.context.gender import gender
from api.context.instrumental import instrumental
from api.context.timbre import timbre
from api.context.tonality import tonality

def approachability_endpoint():
    """Analyze event-based arouseness of the given audio file."""
    return generic_audio_endpoint(approachability, "approachability")

def arouseness_em_endpoint():
    """Analyze event-based arouseness of the given audio file."""
    return generic_audio_endpoint(arouseness_em, "arouseness_em")
    
def arouseness_ev_endpoint():
    """Analyze event-based arouseness of the given audio file."""
    return generic_audio_endpoint(arouseness_ev, "arouseness_ev")

def arouseness_mm_endpoint():
    """Analyze mixed-mode arouseness of the given audio file."""
    return generic_audio_endpoint(arouseness_mm, "arouseness_mm")

def arouseness_mv_endpoint():
    """Analyze multivariable arouseness of the given audio file."""
    return generic_audio_endpoint(arouseness_mv, "arouseness_mv")

def audio_events_endpoint():
    """Analyze audio events in the given audio file."""
    return generic_audio_endpoint(audio_events, "audio_events")

def danceability_endpoint():
    """Analyze the danceability of the given audio file."""
    return generic_audio_endpoint(danceability, "danceability")

def engagement_endpoint():
    """Analyze audience engagement potential of the given audio file."""
    return generic_audio_endpoint(engagement, "engagement")

def gender_endpoint():
    """Analyze gender-related attributes in the given audio file."""
    return generic_audio_endpoint(gender, "gender")

def instrumental_endpoint():
    """Analyze instrumental features of the given audio file."""
    return generic_audio_endpoint(instrumental, "instrumental")

def timbre_endpoint():
    """Analyze timbre features of the given audio file."""
    return generic_audio_endpoint(timbre, "timbre")

def tonality_endpoint():
    """Analyze tonality features of the given audio file."""
    return generic_audio_endpoint(tonality, "tonality")
