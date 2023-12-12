from dotenv import load_dotenv
import os
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

load_dotenv() # Load variables from .env file into environment
API_KEY = os.getenv("API_KEY")
 

def create_database():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_data
                 (city TEXT, temperature REAL, description TEXT)''')
    conn.commit()
    conn.close()

create_database()
