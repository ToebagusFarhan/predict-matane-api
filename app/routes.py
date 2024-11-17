# routes.py
from flask import Blueprint
from controller.predictController import handle_predict_request

user_routes = Blueprint('user_routes', __name__)

user_routes.route("/predict", methods=["POST"])(handle_predict_request)

