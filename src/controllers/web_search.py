import requests
import webbrowser
import os, time
from youtubesearchpython import VideosSearch
from pytube import YouTube
from schemas.schemas import *
from config.settings import *


class Search:
    @staticmethod
    def search_by_google(voice_data):
        try:
            url = f"{GOOGLE_SEARCH_URL}?q={voice_data}"
            webbrowser.get().open(url)
            return voice_data
        except Exception as e:
            return None

    @staticmethod
    def download_youtube_video(voice_data, only_audio=True):
        try:
            t0 = time.perf_counter()

            video_search = VideosSearch(voice_data, limit=1).result()["result"][0][
                "link"
            ]

            if only_audio is False:
                youtube_video = (
                    YouTube(video_search).streams.filter(progressive=True).first()
                )
            else:
                youtube_video = (
                    YouTube(video_search).streams.filter(only_audio=True).first()
                )

            downloaded_file = youtube_video.download()

            if only_audio is True:
                base, _ = os.path.splitext(downloaded_file)
                new_file = base + ".mp3"

                os.rename(downloaded_file, new_file)

            return round(time.perf_counter() - t0, 2)
        except Exception as e:
            print(e)
            return None


class Location:
    def get_ip(self):
        try:
            url = f"{IP_SEARCHER_API_URL}?format=json"

            with requests.get(url) as response:
                if response.status_code == 200:
                    data = response.json()

                    return str(data.get("ip", ""))

                return None
        except Exception as e:
            return None

    def search_location_by_ip(self) -> LocationSchema:
        try:
            ip_address = self.get_ip()

            if ip_address is None:
                return None

            url = f"{GEOLOCATION_API_URL}/json/{ip_address}"

            with requests.get(url) as response:
                if response.status_code == 200:
                    data = response.json()

                    return {
                        "city": data.get("city", ""),
                        "regionName": data.get("region", ""),
                        "country": data.get("country", ""),
                    }

                return None
        except Exception as e:
            return None

    @staticmethod
    def search_by_google_maps(voice_data):
        try:
            url = f"{GOOGLE_MAPS_URL}/{voice_data}"
            webbrowser.get().open(url)
            return voice_data
        except Exception as e:
            print(e)
            return None


class Weather:
    @staticmethod
    def kelvinToCelsius(kelvin):
        return kelvin - 273.15

    def search_weather(self, city=None) -> WeatherSchema:
        try:
            url = f"{OPEN_WEATHER_API_URL}?appid={OPEN_WEATHER_API_TOKEN}&q={city}"

            with requests.get(url) as response:
                open_weather_response = response.json()

                if response.status_code == 200 and open_weather_response["cod"] == 200:
                    y = open_weather_response["main"]

                    current_temperature = y["temp"]
                    current_humidity = y["humidity"]
                    weather_description = open_weather_response["weather"][0][
                        "description"
                    ]

                    return {
                        "temperature": str(
                            round(Weather.kelvinToCelsius(current_temperature), 2)
                        ),
                        "humidity": str(current_humidity),
                        "description": str(weather_description),
                    }

                return None
        except Exception as e:
            return None
