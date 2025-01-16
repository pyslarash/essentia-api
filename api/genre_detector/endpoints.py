from flask import Flask
from api.genre_detector.genre_detector import (discogs_endpoint, discogs_routenote_endpoint, discogs_spotify_endpoint,
                                               jamendo_endpoint, jamendo_routenote_endpoint, jamendo_spotify_endpoint)

routes = [
    ('/genre-detector/discogs', ['POST'], discogs_endpoint),
    ('/genre-detector/discogs-routenote', ['POST'], discogs_routenote_endpoint),
    ('/genre-detector/discogs-spotify', ['POST'], discogs_spotify_endpoint),
    ('/genre-detector/jamendo', ['POST'], jamendo_endpoint),
    ('/genre-detector/jamendo-routenote', ['POST'], jamendo_routenote_endpoint),
    ('/genre-detector/jamendo-spotify', ['POST'], jamendo_spotify_endpoint),
]

def register_genre_detector_routes(app: Flask):
    for route, methods, func in routes:
        app.route(route, methods=methods)(func)