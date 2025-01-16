import logging
import os
from flask import Flask, request, send_from_directory
from functions.detect_device import detect_device
from api.endpoints import register_routes
from flask_cors import CORS, cross_origin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# We'll use a simple lockfile in /tmp
LOCKFILE_PATH = "/tmp/gpu_detected.lock"

def create_app():
    app = Flask(__name__, static_folder='docs')

    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET, POST, OPTIONS"], "allow_headers": "*"}})

    # Handle preflight requests
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = app.response_class()
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            return response

    # Detect GPU/CPU only if our lockfile doesn't exist
    if not os.path.exists(LOCKFILE_PATH):
        detect_device()
        logger.info("GPU detection executed.")
        # Create a lockfile so future workers skip detection
        with open(LOCKFILE_PATH, "w") as lockfile:
            lockfile.write("GPU detected once.\n")
    else:
        pass

    # Register API routes
    register_routes(app)

    # Serve OpenAPI JSON
    @app.route('/docs/openapi.json')
    @cross_origin()
    def serve_openapi():
        return send_from_directory('docs', 'openapi.json')

    # Serve Swagger UI and all static files
    @app.route('/<path:path>')
    def serve_docs(path):
        return send_from_directory('docs', path)

    # Redirect `/docs` to `/docs/index.html`
    @app.route('/', defaults={'path': 'index.html'})
    def serve_docs_index(path):
        return send_from_directory('docs', path)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=9878)

