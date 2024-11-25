# routes.py
from flask import Blueprint
from app.controller.predictController import predict

user_routes = Blueprint('user_routes', __name__)

user_routes.route("/predict", methods=["POST"])(predict)

