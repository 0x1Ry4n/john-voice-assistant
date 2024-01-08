from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv("../../.env"))

CHATBOT_HOST = os.environ.get("CHATBOT_HOST")
CHATBOT_PORT = os.environ.get("CHATBOT_PORT")
GOOGLE_SEARCH_URL = os.environ.get("GOOGLE_SEARCH_URL")
GOOGLE_MAPS_URL = os.environ.get("GOOGLE_MAPS_URL")
OPEN_WEATHER_API_URL = os.environ.get("OPEN_WEATHER_API_URL")
OPEN_WEATHER_API_TOKEN = os.environ.get("OPEN_WEATHER_API_TOKEN")
IP_SEARCHER_API_URL = os.environ.get("IP_SEARCHER_API_URL")
GEOLOCATION_API_URL = os.environ.get("GEOLOCATION_API_URL")
