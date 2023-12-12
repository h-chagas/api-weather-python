import pytest
import requests
from dotenv import load_dotenv
import os
from api_interaction import get_weather, get_all_weather_data, insert_weather_data

load_dotenv()  # Load variables from .env file into environment
API_KEY = os.getenv("API_KEY")

# Mock responses for testing
@pytest.mark.asyncio
async def test_get_weather(monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {'main': {'temp': 20}, 'weather': [{'description': 'clear sky'}]}

    async def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    result = await get_weather(API_KEY, "London")
    assert result == ("London", 8.38, "overcast clouds")
    

def test_database_operations():
    test_data = ("Test_City", 25.5, "Sunny")
    insert_weather_data(test_data)
    data = get_all_weather_data()
    assert test_data in data