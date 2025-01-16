from flask import Flask
from api.process.spotify.spotify import discogs_spotify_pitch_endpoint, jamendo_spotify_pitch_endpoint

routes = [
    ('/process/spotify/discogs', ['POST'], discogs_spotify_pitch_endpoint),
    ('/process/spotify/jamendo', ['POST'], jamendo_spotify_pitch_endpoint),
]

def register_spotify_routes(app: Flask):
    for route, methods, func in routes:
        app.route(route, methods=methods)(func)