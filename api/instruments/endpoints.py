from flask import Flask
from api.instruments.instruments import instruments_endpoint, instruments_spotify_endpoint

routes = [
    ('/instruments/instruments', ['POST'], instruments_endpoint),
    ('/instruments/instruments-spotify', ['POST'], instruments_spotify_endpoint),
]

def register_instruments_routes(app: Flask):
    for route, methods, func in routes:
        app.route(route, methods=methods)(func)