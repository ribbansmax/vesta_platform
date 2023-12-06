from app import app
from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for, flash
from datetime import datetime
import pytz
from .vestaboard_api import send_to_vestaboard
import ipinfo
from dotenv import load_dotenv
import os
from better_profanity import profanity

def check_for_quiet_hours():
    # Define the CST timezone
    cst = pytz.timezone('America/Chicago')
    
    # Get the current time in CST
    current_time = datetime.now(cst).time()

    # Define quiet hours (outside 10AM to 10PM CST)
    start_time = datetime.strptime('10:00:00', '%H:%M:%S').time()
    end_time = datetime.strptime('22:00:00', '%H:%M:%S').time()

    # Return True if current time is outside of allowed hours, otherwise False
    return not (start_time <= current_time <= end_time)

def get_city(ip):
    app.logger.info("Client IP: %s", ip)
    print(f'Client IP: {ip}')

    load_dotenv()
    IPINFO_ACCESS_TOKEN = os.getenv("IPINFO_ACCESS_TOKEN")
    handler = ipinfo.getHandler(IPINFO_ACCESS_TOKEN)
    details = handler.getDetails(ip)
    city = details.all.get("city") or 'local'

    app.logger.info("Client city: %s", city)
    print(f'Client city: {city}')
    return city

@app.route('/')
def index():
    message = request.args.get('message', '')  # Retrieve the message if it exists
    return render_template('index.html', message=message)

@app.route('/send-message', methods=['POST'])
def handle_message():
    if check_for_quiet_hours():
        return redirect(url_for('index', message='Failed to send message: please try again during the hours of 10AM to 10PM CST to not wake anyone up'))
    # Concatenate the contents of the five input fields
    message_lines = [
        request.form.get(f'input{i}', '').ljust(22) for i in range(1, 6)
    ]
    message = ''.join(message_lines).strip()  # Combine and remove trailing whitespace
    print(f'Message: {message}')
    if profanity.contains_profanity(message):
        print(f'Message contains profanity: {message}')
        censored_message = profanity.censor(message, '-')
    else:
        censored_message = message
    from_name = request.form['from']
    if not from_name:
        # Capture the user's IP address
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        from_name = get_city(user_ip)
    # Process your message as needed and call send_to_vestaboard
    response = send_to_vestaboard(censored_message, from_name)
    if response and response.status_code == 200:
        return redirect(url_for('index', message='Message sent successfully!'))
    else:
        return redirect(url_for('index', message='Failed to send message.'))