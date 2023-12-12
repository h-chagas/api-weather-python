import aiohttp
import asyncio
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()  # Load variables from .env file into environment
API_KEY = os.getenv("API_KEY")
city = "Mozambique"

async def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                print("--> OK")
                data = await response.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                print("---->", data)
                return city, temp, description
            else:
                raise Exception("API request failed")

async def main():
    try:
        result = await get_weather(API_KEY, city)
        print("Weather in", result[0], ": Temperature =", result[1], "°C, Description =", result[2])
        insert_weather_data(result)
        get_all_weather_data()
    except Exception as e:
        print("Error:", e)

def insert_weather_data(data):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS weather_data (city TEXT, temperature REAL, description TEXT)')
    c.execute('INSERT INTO weather_data VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()
    print("---> INSERTED!")

def get_all_weather_data():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('SELECT * FROM weather_data')
    data = c.fetchall()
    conn.close()
    print("-->", data)
    return data

if __name__ == "__main__":
    asyncio.run(main())

