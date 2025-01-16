from functions.generic_audio_endpoint import generic_audio_endpoint
from api.process.track_analysis import track_analysis
from api.process.track_data import process_audio_file

def track_analysis_endpoint():
    return generic_audio_endpoint(track_analysis, "track_analysis")

def track_data_endpoint():
    return generic_audio_endpoint(process_audio_file, "track_data")