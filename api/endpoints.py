from flask import Flask
from api.genre_detector.endpoints import routes as genre_detector_routes
from api.music_cultures.endpoints import routes as music_cultures_routes
from api.song_styles.endpoints import routes as song_styles_routes
from api.context.endpoints import routes as context_routes
from api.instruments.endpoints import routes as instrument_routes
from api.mood.endpoints import routes as mood_routes
from api.process.spotify.endpoints import routes as spotify_routes
from api.process.endpoints import routes as process_routes

def register_routes(app: Flask):
    """
    Register all routes with the app.
    """
    # Register user routes with `/api` prefix
    register_routes_with_prefix(app, "/api")
    
def register_routes_with_prefix(app: Flask, prefix: str):
    
    for route, methods, func in genre_detector_routes:
        app.route(f"{prefix}{route}", methods=methods)(func)
        
    for route, methods, func in music_cultures_routes:
        app.route(f"{prefix}{route}", methods=methods)(func)
        
    for route, methods, func in song_styles_routes:
        app.route(f"{prefix}{route}", methods=methods)(func)
        
    for route, methods, func in context_routes:
        app.route(f"{prefix}{route}", methods=methods)(func)
        
    for route, methods, func in instrument_routes:
        app.route(f"{prefix}{route}", methods=methods)(func)
        
    for route, methods, func in mood_routes:
        app.route(f"{prefix}{route}", methods=methods)(func)
        
    for route, methods, func in spotify_routes:
        app.route(f"{prefix}{route}", methods=methods)(func)
        
    for route, methods, func in process_routes:
        app.route(f"{prefix}{route}", methods=methods)(func)