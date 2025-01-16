from flask import Flask
from api.context.context import (approachability_endpoint, arouseness_em_endpoint, arouseness_ev_endpoint,
                                    arouseness_mm_endpoint, arouseness_mv_endpoint, audio_events_endpoint,
                                    danceability_endpoint, engagement_endpoint, gender_endpoint, instrumental_endpoint,
                                    timbre_endpoint, tonality_endpoint
                                )

routes = [
    ('/context/approachability', ['POST'], approachability_endpoint),
    ('/context/arouseness-emomusic-musicnn', ['POST'], arouseness_em_endpoint),
    ('/context/arouseness-emomusic-vggish', ['POST'], arouseness_ev_endpoint),
    ('/context/arouseness-muse-musicnn', ['POST'], arouseness_mm_endpoint),
    ('/context/arouseness-muse-vggish', ['POST'], arouseness_mv_endpoint),
    ('/context/audio-events', ['POST'], audio_events_endpoint),
    ('/context/danceability', ['POST'], danceability_endpoint),
    ('/context/engagement', ['POST'], engagement_endpoint),
    ('/context/gender', ['POST'], gender_endpoint),
    ('/context/instrumental', ['POST'], instrumental_endpoint),
    ('/context/timbre', ['POST'], timbre_endpoint),
    ('/context/tonality', ['POST'], tonality_endpoint),
]

def register_context_routes(app: Flask):
    for route, methods, func in routes:
        app.route(route, methods=methods)(func)