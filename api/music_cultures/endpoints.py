from flask import Flask
from api.music_cultures.music_cultures import discogs_music_cultures_endpoint, jamendo_music_cultures_endpoint

routes = [
    ('/music-cultures/discogs-spotify', ['POST'], discogs_music_cultures_endpoint),
    ('/music-cultures/jamendo-spotify', ['POST'], jamendo_music_cultures_endpoint),
]

def register_music_cultures_routes(app: Flask):
    for route, methods, func in routes:
        app.route(route, methods=methods)(func)