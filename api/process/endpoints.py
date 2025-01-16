from flask import Flask
from api.process.process import track_analysis_endpoint, track_data_endpoint

routes = [
    ('/process/track-analysis', ['POST'], track_analysis_endpoint),
    ('/process/track-data', ['POST'], track_data_endpoint),
]

def register_process_routes(app: Flask):
    for route, methods, func in routes:
        app.route(route, methods=methods)(func)