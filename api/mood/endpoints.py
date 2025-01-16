from flask import Flask
from api.mood.mood import (acoustic_endpoint, aggressive_endpoint, electronic_endpoint, happy_endpoint,
                           jamendo_mood_spotify_endpoint, jamendo_mood_theme_endpoint, mirex_endpoint,
                           party_endpoint, relaxed_endpoint, sad_endpoint)

routes = [
    ('/mood/acoustic', ['POST'], acoustic_endpoint),
    ('/mood/aggressive', ['POST'], aggressive_endpoint),
    ('/mood/electronic', ['POST'], electronic_endpoint),
    ('/mood/happy', ['POST'], happy_endpoint),
    ('/mood/spotify', ['POST'], jamendo_mood_spotify_endpoint),
    ('/mood/jamendo-mood-theme', ['POST'], jamendo_mood_theme_endpoint),
    ('/mood/mirex', ['POST'], mirex_endpoint),
    ('/mood/party', ['POST'], party_endpoint),
    ('/mood/relaxed', ['POST'], relaxed_endpoint),
    ('/mood/sad', ['POST'], sad_endpoint),
]

def register_mood_routes(app: Flask):
    for route, methods, func in routes:
        app.route(route, methods=methods)(func)