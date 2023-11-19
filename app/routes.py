from app import app
from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for, flash
from .vestaboard_api import send_to_vestaboard

# bp = Blueprint('routes', __name__)

@app.route('/')
def index():
    message = request.args.get('message', '')  # Retrieve the message if it exists
    return render_template('index.html', message=message)

@app.route('/send-message', methods=['POST'])
def handle_message():
    message = request.form['message']
    from_name = request.form['from']
    # Process your message as needed and call send_to_vestaboard
    response = send_to_vestaboard(message, from_name)
    if response and response.status_code == 200:
        return redirect(url_for('index', message='Message sent successfully!'))
    else:
        return redirect(url_for('index', message='Failed to send message.'))