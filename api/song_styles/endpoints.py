from flask import Flask
from api.song_styles.song_styles import discogs_song_styles_endpoint, jamendo_song_styles_endpoint

routes = [
    ('/song-styles/discogs-spotify', ['POST'], discogs_song_styles_endpoint),
    ('/song-styles/jamendo-spotify', ['POST'], jamendo_song_styles_endpoint),
]

def register_song_styles_routes(app: Flask):
    for route, methods, func in routes:
        app.route(route, methods=methods)(func)