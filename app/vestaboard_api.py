# vestaboard_api.py
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
VESTABOARD_API_KEY = os.getenv("VESTABOARD_API_KEY")
# Vestaboard character dictionary
vestaboard_characters = {
  "Blank": 0,
  "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
  "J": 10, "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19,
  "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26,
  "1": 27, "2": 28, "3": 29, "4": 30, "5": 31, "6": 32, "7": 33, "8": 34, "9": 35, "0": 36,
  "!": 37, "@": 38, "#": 39, "$": 40, "(": 41, ")": 42,
  "-": 44, "+": 46, "&": 47, "=": 48, ";": 49, ":": 50,
  "'": 52, "\"": 53, "%": 54, ",": 55, ".": 56, "/": 59, "?": 60,
  "°": 62, "Red": 63, "Orange": 64, "Yellow": 65, "Green": 66,
  "Blue": 67, "Violet": 68, "White": 69, "Black": 70, "Filled": 71
}

def string_to_vestaboard_codes(input_string):

    upper_string = input_string.upper()
    codes = []

    for char in upper_string:
        if char == " ":
            codes.append(str(vestaboard_characters["Blank"]))
        elif char in vestaboard_characters:
            codes.append(str(vestaboard_characters[char]))
        else:
            codes.append(str(vestaboard_characters["Blank"]))  # default for unknown chars

    return codes

def format_for_vestaboard(input_string):
    """
    Formats a string into a 6x22 Vestaboard grid.
    """
    # Convert the string to Vestaboard character codes
    codes = string_to_vestaboard_codes(input_string)

    # Initialize a 6x22 grid with all zeros (blank)
    grid = [[0 for _ in range(22)] for _ in range(6)]

    # Place the codes into the grid
    row, col = 0, 1  # Starting position, adjust as needed
    for code in codes:
        grid[row][col] = code
        col += 1
        if col >= 22:  # Move to the next row if the end of the row is reached
            col = 0
            row += 1
            if row >= 6:  # Stop if the grid is full
                break

    return grid

def send_to_vestaboard(message):
    """
    Sends a message to the Vestaboard.
    """
    # Format the message for the Vestaboard
    formatted_message = format_for_vestaboard(message)

    # URL for the Vestaboard API
    url = "https://rw.vestaboard.com/"

    # Headers including the API key
    headers = {
        "Content-Type": "application/json",
        "X-Vestaboard-Read-Write-Key": VESTABOARD_API_KEY
    }

    try:
        # Make the POST request to the Vestaboard API
        response = requests.post(url, headers=headers, data=json.dumps(formatted_message))

        # Check if the request was successful
        if response.status_code == 200:
            print("Message successfully sent to Vestaboard.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

        return response.json()

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred: {e}")