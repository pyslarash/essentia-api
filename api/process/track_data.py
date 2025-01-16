# ------------------------
# 1) Import the Classifiers
# ------------------------
from classes.track_analysis import TrackAnalysis
from classes.discogs_genres import DiscogsGenreClassifier
from classes.jamendo_genres import JamendoGenreClassifier
from classes.jamendo_instruments import JamendoInstrumentClassifier
from classes.approachability import ApproachabilityClassifier
from classes.arousal_valence_emomusic_musicnn import ArousalValenceEmomusicMusiCNNClassifier
from classes.arousal_valence_emomusic_vggish import ArousalValenceEmomusicVggishClassifier
from classes.arousal_valence_muse_musicnn import ArousalValenceMuseMusiCNNClassifier
from classes.arousal_valence_muse_vggish import ArousalValenceMuseVggishClassifier
from classes.yamnet_audio_event import YamNetAudioEventClassifier
from classes.danceability import DanceabilityClassifier
from classes.engagement import EngagementClassifier
from classes.voice_instrumental import VoiceInstrumentalClassifier
from classes.voice_gender import VoiceGenderClassifier
from classes.timbre import TimbreClassifier
from classes.tonality import TonalityClassifier
from classes.mood_acoustic import MoodAcousticClassifier
from classes.mood_aggressive import MoodAggressiveClassifier
from classes.mood_electronic import MoodElectronicClassifier
from classes.mood_happy import MoodHappyClassifier
from classes.mood_party import MoodPartyClassifier
from classes.mood_relaxed import MoodRelaxedClassifier
from classes.mood_sad import MoodSadClassifier
from classes.jamendo_mood_and_theme import JamendoMoodAndThemeClassifier
from classes.moods_mirex import MoodsMirexClassifier

# ------------------------
# 2) Import the Mappings
# ------------------------
from maps.discogs_to_music_cultures import discogs_to_music_cultures
from maps.jamendo_to_music_cultures import jamendo_to_music_cultures
from maps.discogs_to_routenote import discogs_to_routenote
from maps.discogs_to_spotify import discogs_to_spotify
from maps.jamendo_to_routenote import jamendo_to_routenote
from maps.jamendo_to_spotify import jamendo_to_spotify
from maps.discogs_to_song_styles import discogs_to_song_styles
from maps.jamendo_to_song_styles import jamendo_to_song_styles
from maps.jamendo_to_instruments import jamendo_to_instruments
from maps.jamendo_to_moods import jamendo_to_moods

# =============================================================================
# Helper functions to handle mapping rules
# =============================================================================

def _ensure_list(value):
    """
    If `value` is a single string, convert it to a list of one element.
    If `value` is already a list, leave it as is.
    If `value` is None or empty, return an empty list.
    """
    if not value:
        return []
    if isinstance(value, list):
        return value
    # Otherwise, assume it's a string
    return [value]


def _unique_and_slice(values, max_count=2, default_if_empty="None of these"):
    """
    1. Remove duplicates from `values` while preserving order.
    2. Slice to `max_count`.
    3. If there's nothing left, return [default_if_empty].
    """
    unique_vals = []
    for val in values:
        if val not in unique_vals:
            unique_vals.append(val)

    unique_vals = unique_vals[:max_count]  # slice to max_count
    return unique_vals if unique_vals else [default_if_empty]


def map_all_genres(mapping_dict, genres_list, max_count=2):
    """
    Given a dictionary `mapping_dict` and a list of up to three genres (e.g. [main, primary, secondary]),
    this function:
      - Looks up each genre in `mapping_dict`; if not found => "Unknown"
      - If result != "Unknown", we convert to a list (if needed) and add it
      - Remove duplicates, slice to `max_count`, and if empty => ["None of these"].

    Returns:
      list of mapped items (or ["None of these"] if nothing valid is found)
    """
    all_items = []

    for genre in genres_list:
        if genre:
            # Look up the mapping (default "Unknown" if not present)
            mapped = mapping_dict.get(genre, "Unknown")
            if mapped != "Unknown":
                # Convert to list if needed
                mapped_list = mapped if isinstance(mapped, list) else [mapped]
                all_items.extend(mapped_list)

    # Remove duplicates, preserving order
    seen = []
    for item in all_items:
        if item not in seen:
            seen.append(item)

    # Slice to max_count
    final = seen[:max_count]

    # If none remain, return ["None of these"]
    return final if final else ["None of these"]

def map_moods(mapping_dict, mood_list, max_count=2):
    """
    For a *list* of moods (e.g. top3 from Jamendo mood/theme),
    we map each mood and gather them all into one final set/list
    with duplicates removed, then sliced to `max_count`.

    If no valid mappings, returns ['None of these'].
    """
    if not mood_list:
        return ["None of these"]

    all_mapped = []
    for mood in mood_list:
        mapped = mapping_dict.get(mood, None)
        if not mapped:
            # If there's no mapping, we follow the rule => 'None of these'
            mapped = "None of these"
        # Add to list, converting to list if needed
        all_mapped.extend(_ensure_list(mapped))

    return _unique_and_slice(all_mapped, max_count=max_count, default_if_empty="None of these")


# =============================================================================
# Main function
# =============================================================================
def process_audio_file(audio_file: str):
    """
    Performs the entire analysis process on `audio_file` using all the classifiers
    and mappings you have in your system. Returns a dictionary of results.

    Args:
        audio_file (str): Path to an audio file, e.g. "files/audio.wav"

    Returns:
        dict: Consolidated results from all classifiers + mappings
    """

    # -----------------------------------------------------------------
    # PART A: Extract Basic Track Analysis
    # -----------------------------------------------------------------
    track_analysis_extractor = TrackAnalysis()
    try:
        track_features = track_analysis_extractor.extract_features(audio_file)
    except Exception as e:
        print(f"[Warning] TrackAnalysis error: {e}")
        track_features = {}

    # -----------------------------------------------------------------
    # PART B: Classify (Discogs) Genres
    # -----------------------------------------------------------------
    discogs_classifier = DiscogsGenreClassifier()
    try:
        discogs_main_genre, discogs_primary_genre, discogs_secondary_genre = discogs_classifier.classify_genres(audio_file)
    except Exception as e:
        print(f"[Warning] DiscogsGenreClassifier error: {e}")
        discogs_main_genre, discogs_primary_genre, discogs_secondary_genre = None, None, None
    
    # Now gather them in a small list
    discogs_genres_list = []
    if discogs_main_genre:
        discogs_genres_list.append(discogs_main_genre)
    if discogs_primary_genre:
        discogs_genres_list.append(discogs_primary_genre)
    if discogs_secondary_genre:
        discogs_genres_list.append(discogs_secondary_genre)

    # Or simply:
    # discogs_genres_list = [g for g in (discogs_main_genre, discogs_primary_genre, discogs_secondary_genre) if g]

    # Now map all three for each category:

    # --- Music Cultures (up to 2) ---
    discogs_music_cultures = map_all_genres(discogs_to_music_cultures, discogs_genres_list, max_count=2)

    # --- Spotify (up to 3) ---
    discogs_spotify_genres = map_all_genres(discogs_to_spotify, discogs_genres_list, max_count=3)

    # --- RouteNote (up to 2) ---
    discogs_routenote_genres = map_all_genres(discogs_to_routenote, discogs_genres_list, max_count=2)

    # --- Song Styles (up to 2) ---
    discogs_song_styles = map_all_genres(discogs_to_song_styles, discogs_genres_list, max_count=2)

    discogs_mappings = {
        "spotify_music_cultures": discogs_music_cultures,
        "spotify_genres": discogs_spotify_genres,
        "routenote_genres": discogs_routenote_genres,
        "spotify_song_styles": discogs_song_styles
    }

    # -----------------------------------------------------------------
    # PART C: Classify (Jamendo) Genres
    # -----------------------------------------------------------------
    jamendo_classifier = JamendoGenreClassifier()
    try:
        jamendo_primary_genre, jamendo_secondary_genre, jamendo_tertiary_genre = jamendo_classifier.classify_genres(audio_file)
    except Exception as e:
        print(f"[Warning] JamendoGenreClassifier error: {e}")
        jamendo_primary_genre, jamendo_secondary_genre, jamendo_tertiary_genre = None, None, None
    
    # Combine them similarly
    jamendo_genres_list = [g for g in (jamendo_primary_genre, jamendo_secondary_genre, jamendo_tertiary_genre) if g]

    # Now map them:
    jamendo_music_cultures = map_all_genres(jamendo_to_music_cultures, jamendo_genres_list, max_count=2)
    jamendo_spotify_genres = map_all_genres(jamendo_to_spotify, jamendo_genres_list, max_count=3)
    jamendo_routenote_genres = map_all_genres(jamendo_to_routenote, jamendo_genres_list, max_count=2)
    jamendo_song_styles = map_all_genres(jamendo_to_song_styles, jamendo_genres_list, max_count=2)

    jamendo_mappings = {
        "music_cultures": jamendo_music_cultures,
        "spotify": jamendo_spotify_genres,
        "routenote": jamendo_routenote_genres,
        "song_styles": jamendo_song_styles
    }

    # -----------------------------------------------------------------
    # PART D: Classify Instruments (Jamendo)
    # -----------------------------------------------------------------
    jamendo_instrument_classifier = JamendoInstrumentClassifier()
    try:
        instruments_detected = jamendo_instrument_classifier.classify_instruments(audio_file)
    except Exception as e:
        print(f"[Warning] JamendoInstrumentClassifier error: {e}")
        instruments_detected = []

    # Map instruments to our own standard instrument names
    # (Remove duplicates if any)
    instruments_mapped_temp = []
    for instr in instruments_detected:
        mapped_instr = jamendo_to_instruments.get(instr, "None of these")
        instruments_mapped_temp.extend(_ensure_list(mapped_instr))

    # Remove duplicates
    instruments_mapped = _unique_and_slice(instruments_mapped_temp, max_count=999)  # no limit specified, so pass a big number

    # -----------------------------------------------------------------
    # PART E: Classify Mood & Theme (Jamendo)
    # -----------------------------------------------------------------
    jamendo_mood_theme_classifier = JamendoMoodAndThemeClassifier()
    try:
        jamendo_mood_theme_top3 = jamendo_mood_theme_classifier.classify_mood_and_theme(audio_file, top_n=3)
    except Exception as e:
        print(f"[Warning] JamendoMoodAndThemeClassifier error: {e}")
        jamendo_mood_theme_top3 = []

    # Map the top3 moods/themes => up to 2 final mapped values
    jamendo_mood_theme_mapped = map_moods(jamendo_to_moods, jamendo_mood_theme_top3, max_count=2)

    # -----------------------------------------------------------------
    # PART F: Classify Danceability (VGGish)
    # -----------------------------------------------------------------
    danceability_classifier = DanceabilityClassifier()
    try:
        danceability_scores = danceability_classifier.classify_danceability(audio_file)
    except Exception as e:
        print(f"[Warning] DanceabilityClassifier error: {e}")
        danceability_scores = {}

    # -----------------------------------------------------------------
    # PART G: Classify Audio Events (YamNet)
    # -----------------------------------------------------------------
    yamnet_classifier = YamNetAudioEventClassifier()
    try:
        yamnet_events_top10 = yamnet_classifier.classify_audio_events(audio_file)
    except Exception as e:
        print(f"[Warning] YamNetAudioEventClassifier error: {e}")
        yamnet_events_top10 = []

    # -----------------------------------------------------------------
    # PART H: Additional Classifiers (Approachability, Arousal/Valence, etc.)
    # -----------------------------------------------------------------

    # 1) Approachability
    approachability_classifier = ApproachabilityClassifier()
    try:
        approachability_score = approachability_classifier.classify_approachability(audio_file)
    except Exception as e:
        print(f"[Warning] ApproachabilityClassifier error: {e}")
        approachability_score = None

    # 2) Arousal & Valence (EmoMusic + MusiCNN)
    av_emomusic_musicnn_cls = ArousalValenceEmomusicMusiCNNClassifier()
    try:
        av_emomusic_musicnn = av_emomusic_musicnn_cls.classify_arousal_valence(audio_file)
    except Exception as e:
        print(f"[Warning] ArousalValenceEmomusicMusiCNNClassifier error: {e}")
        av_emomusic_musicnn = None

    # 3) Arousal & Valence (EmoMusic + VGGish)
    av_emomusic_vggish_cls = ArousalValenceEmomusicVggishClassifier()
    try:
        av_emomusic_vggish = av_emomusic_vggish_cls.classify_arousal_valence(audio_file)
    except Exception as e:
        print(f"[Warning] ArousalValenceEmomusicVggishClassifier error: {e}")
        av_emomusic_vggish = None

    # 4) Arousal & Valence (Muse + MusiCNN)
    av_muse_musicnn_cls = ArousalValenceMuseMusiCNNClassifier()
    try:
        av_muse_musicnn = av_muse_musicnn_cls.classify_arousal_valence(audio_file)
    except Exception as e:
        print(f"[Warning] ArousalValenceMuseMusiCNNClassifier error: {e}")
        av_muse_musicnn = None

    # 5) Arousal & Valence (Muse + VGGish)
    av_muse_vggish_cls = ArousalValenceMuseVggishClassifier()
    try:
        av_muse_vggish = av_muse_vggish_cls.classify_arousal_valence(audio_file)
    except Exception as e:
        print(f"[Warning] ArousalValenceMuseVggishClassifier error: {e}")
        av_muse_vggish = None

    # 6) Engagement Classifier
    engagement_classifier = EngagementClassifier()
    try:
        engagement_score = engagement_classifier.classify_engagement(audio_file)
    except Exception as e:
        print(f"[Warning] EngagementClassifier error: {e}")
        engagement_score = None

    # 7) Voice / Instrumental
    voice_instrumental_classifier = VoiceInstrumentalClassifier()
    try:
        voice_instrumental_result = voice_instrumental_classifier.classify_voice_instrumental(audio_file)
    except Exception as e:
        print(f"[Warning] VoiceInstrumentalClassifier error: {e}")
        voice_instrumental_result = None

    # 8) Voice Gender
    voice_gender_classifier = VoiceGenderClassifier()
    try:
        voice_gender_result = voice_gender_classifier.classify_gender(audio_file)
    except Exception as e:
        print(f"[Warning] VoiceGenderClassifier error: {e}")
        voice_gender_result = None

    # 9) Timbre
    timbre_classifier = TimbreClassifier()
    try:
        timbre_result = timbre_classifier.classify_timbre(audio_file)
    except Exception as e:
        print(f"[Warning] TimbreClassifier error: {e}")
        timbre_result = None

    # 10) Tonality
    tonality_classifier = TonalityClassifier()
    try:
        tonality_result = tonality_classifier.classify_tonality(audio_file)
    except Exception as e:
        print(f"[Warning] TonalityClassifier error: {e}")
        tonality_result = None

    # 11) Mood Acoustic
    mood_acoustic_classifier = MoodAcousticClassifier()
    try:
        # NOTE: The code snippet uses `classify_mood`, not `classify_mood_acoustic`.
        mood_acoustic_scores = mood_acoustic_classifier.classify_mood(audio_file)  
    except Exception as e:
        print(f"[Warning] MoodAcousticClassifier error: {e}")
        mood_acoustic_scores = None

    # 12) Mood Aggressive
    mood_aggressive_classifier = MoodAggressiveClassifier()
    try:
        mood_aggressive_scores = mood_aggressive_classifier.classify_mood(audio_file)
    except Exception as e:
        print(f"[Warning] MoodAggressiveClassifier error: {e}")
        mood_aggressive_scores = None

    # 13) Mood Electronic
    mood_electronic_classifier = MoodElectronicClassifier()
    try:
        mood_electronic_scores = mood_electronic_classifier.classify_mood(audio_file)
    except Exception as e:
        print(f"[Warning] MoodElectronicClassifier error: {e}")
        mood_electronic_scores = None

    # 14) Mood Happy
    mood_happy_classifier = MoodHappyClassifier()
    try:
        mood_happy_scores = mood_happy_classifier.classify_mood(audio_file)
    except Exception as e:
        print(f"[Warning] MoodHappyClassifier error: {e}")
        mood_happy_scores = None

    # 15) Mood Party
    mood_party_classifier = MoodPartyClassifier()
    try:
        mood_party_scores = mood_party_classifier.classify_mood(audio_file)
    except Exception as e:
        print(f"[Warning] MoodPartyClassifier error: {e}")
        mood_party_scores = None

    # 16) Mood Relaxed
    mood_relaxed_classifier = MoodRelaxedClassifier()
    try:
        mood_relaxed_scores = mood_relaxed_classifier.classify_mood(audio_file)
    except Exception as e:
        print(f"[Warning] MoodRelaxedClassifier error: {e}")
        mood_relaxed_scores = None

    # 17) Mood Sad
    mood_sad_classifier = MoodSadClassifier()
    try:
        mood_sad_scores = mood_sad_classifier.classify_mood(audio_file)
    except Exception as e:
        print(f"[Warning] MoodSadClassifier error: {e}")
        mood_sad_scores = None

    # 18) Moods Mirex
    moods_mirex_classifier = MoodsMirexClassifier()
    try:
        moods_mirex_result = moods_mirex_classifier.classify_moods(audio_file)
    except Exception as e:
        print(f"[Warning] MoodsMirexClassifier error: {e}")
        moods_mirex_result = None

    # -----------------------------------------------------------------
    # PART I: Build the Final Dictionary
    # -----------------------------------------------------------------
    results = {
        "track_analysis": track_features,
        "discogs_genres": {
            "main_genre": discogs_main_genre,
            "primary_genre": discogs_primary_genre,
            "secondary_genre": discogs_secondary_genre,
            "mappings": discogs_mappings
        },
        "jamendo_genres": {
            "primary_genre": jamendo_primary_genre,
            "secondary_genre": jamendo_secondary_genre,
            "tertiary_genre": jamendo_tertiary_genre,
            "mappings": jamendo_mappings
        },
        "instruments": {
            "detected": instruments_detected,
            "spotify_mapped": instruments_mapped
        },
        "moods_themes": {
            "top3": jamendo_mood_theme_top3,
            "spotify_mapped": jamendo_mood_theme_mapped
        },
        "danceability_scores": danceability_scores,
        "yamnet_audio_events_top10": yamnet_events_top10,
        "approachability_scores": approachability_score,
        "arousal_valence": {
            "emomusic_musicnn": av_emomusic_musicnn,
            "emomusic_vggish":  av_emomusic_vggish,
            "muse_musicnn":     av_muse_musicnn,
            "muse_vggish":      av_muse_vggish
        },
        "engagement_scores": engagement_score,
        "voice_instrumental_result": voice_instrumental_result,
        "voice_gender_result": voice_gender_result,
        "timbre_result": timbre_result,
        "tonality_result": tonality_result,
        "mood_acoustic_result": mood_acoustic_scores,
        "mood_aggressive_result": mood_aggressive_scores,
        "mood_electronic_result": mood_electronic_scores,
        "mood_happy_result": mood_happy_scores,
        "mood_party_result": mood_party_scores,
        "mood_relaxed_result": mood_relaxed_scores,
        "mood_sad_result": mood_sad_scores,
        "moods_mirex_result": moods_mirex_result
    }

    return results


def main():
    """
    Example usage. You can adapt this to your own environment.
    """
    audio_file = "files/audio.wav"       # Update with your audio path

    try:
        final_results = process_audio_file(audio_file)
        # Print or handle the final results:
        print("============= FINAL RESULTS =============")
        for key, val in final_results.items():
            print(f"{key} => {val}")
    except Exception as e:
        print(f"[Error] Could not process audio file: {e}")


if __name__ == "__main__":
    main()
