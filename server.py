# server.py
import os
from flask import Flask
from app.routes import user_routes

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.register_blueprint(user_routes)

if __name__ == '__main__':
    # Get the port from the environment variable (default to 8080 for Cloud Run)
    port = int(os.environ.get("PORT", 8080))
    # Use '0.0.0.0' as the host to allow external access in Cloud Run
    app.run(host='0.0.0.0', port=port)
