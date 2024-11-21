# server.py
from flask import Flask
from app.routes import user_routes

app = Flask(__name__)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)