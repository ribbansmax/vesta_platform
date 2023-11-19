from app import app
from flask import Flask, Blueprint, request, jsonify, render_template
from .vestaboard_api import send_to_vestaboard

# bp = Blueprint('routes', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def handle_message():
    message = request.form['message']
    from_name = request.form['from']
    # Process your message as needed and call send_to_vestaboard
    send_to_vestaboard(message, from_name)
    return "Message sent successfully!"