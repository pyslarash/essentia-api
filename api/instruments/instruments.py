from functions.generic_audio_endpoint import generic_audio_endpoint
from api.instruments.instrument_detector import instrument_detector
from api.instruments.instrument_detector_spotify import instrument_detector_spotify
    
def instruments_endpoint():
    """
    Classify genres for the given audio file and return Discogs results in JSON format.
    """
    return generic_audio_endpoint(instrument_detector, "instruments")

def instruments_spotify_endpoint():
    """
    Classify genres for the given audio file and return Discogs results in JSON format.
    """
    return generic_audio_endpoint(instrument_detector_spotify, "spotify_instruments")