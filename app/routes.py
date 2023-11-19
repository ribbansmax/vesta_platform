from app import app
from flask import Flask, Blueprint, request, jsonify
from .vestaboard_api import send_to_vestaboard

# bp = Blueprint('routes', __name__)

@app.route('/')
def home():
    # Extract question from request
    return "hello world"