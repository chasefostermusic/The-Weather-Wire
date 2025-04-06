#!/usr/bin/env python3
import requests
import time
import datetime
from pythonosc import udp_client
import json
import sys
import os
import logging
from logging.handlers import RotatingFileHandler

# Set up logging
log_dir = os.path.expanduser('~/Library/Logs/The Weather Wire')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'weather_wire.log')

# Configure logging to both file and console
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3)
console_handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    handlers=[handler, console_handler],
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# List of 20 biggest cities with their coordinates
CITIES = [
    {"name": "TOKYO", "lat": 35.6762, "lon": 139.6503},
    {"name": "DELHI", "lat": 28.6139, "lon": 77.2090},
    {"name": "SHANGHAI", "lat": 31.2304, "lon": 121.4737},
    {"name": "SAO PAULO", "lat": -23.5505, "lon": -46.6333},
    {"name": "MEXICO CITY", "lat": 19.4326, "lon": -99.1332},
    {"name": "CAIRO", "lat": 30.0444, "lon": 31.2357},
    {"name": "MUMBAI", "lat": 19.0760, "lon": 72.8777},
    {"name": "BEIJING", "lat": 39.9042, "lon": 116.4074},
    {"name": "DHAKA", "lat": 23.8103, "lon": 90.4125},
    {"name": "OSAKA", "lat": 34.6937, "lon": 135.5023},
    {"name": "CHONGQING", "lat": 29.4316, "lon": 106.9123},
    {"name": "ISTANBUL", "lat": 41.0082, "lon": 28.9784},
    {"name": "KARACHI", "lat": 24.8608, "lon": 67.0104},
    {"name": "KINSHASA", "lat": -4.4419, "lon": 15.2663},
    {"name": "LAGOS", "lat": 6.5244, "lon": 3.3792},
    {"name": "MANILA", "lat": 14.5995, "lon": 120.9842},
    {"name": "TIANJIN", "lat": 39.3434, "lon": 117.3616},
    {"name": "GUANGZHOU", "lat": 23.1291, "lon": 113.2644},
    {"name": "LOS ANGELES", "lat": 34.0522, "lon": -118.2437},
    {"name": "MOSCOW", "lat": 55.7558, "lon": 37.6173}
]

class WeatherWire:
    def __init__(self):
        try:
            logging.info("Initializing UDP client on 127.0.0.1:7000")
            self.client = udp_client.SimpleUDPClient("127.0.0.1", 7000)
            self.current_city_index = 0
            self.base_url = "https://api.open-meteo.com/v1/forecast"
            
            # Test OSC connection
            logging.info("Testing OSC connection...")
            self.client.send_message("/test", "connection_test")
            logging.info("OSC test message sent")
        except Exception as e:
            logging.error(f"Error initializing WeatherWire: {e}")
            raise

    def get_weather_data(self, city):
        params = {
            "latitude": city["lat"],
            "longitude": city["lon"],
            "current": ["temperature_2m", "wind_speed_10m", "relative_humidity_2m", "weather_code"],
            "timezone": "auto"
        }
        
        try:
            logging.info(f"Fetching weather data for {city['name']}...")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Successfully fetched weather data for {city['name']}: {json.dumps(data['current'])}")
            return data
        except requests.RequestException as e:
            logging.error(f"Error fetching weather data for {city['name']}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error fetching weather data for {city['name']}: {e}")
            return None

    def get_weather_description(self, weather_code):
        weather_codes = {
            0: "CLEAR SKY",
            1: "MAINLY CLEAR",
            2: "PARTLY CLOUDY",
            3: "OVERCAST",
            45: "FOGGY",
            48: "DEPOSITING RIME FOG",
            51: "LIGHT DRIZZLE",
            53: "MODERATE DRIZZLE",
            55: "DENSE DRIZZLE",
            61: "SLIGHT RAIN",
            63: "MODERATE RAIN",
            65: "HEAVY RAIN",
            71: "SLIGHT SNOW",
            73: "MODERATE SNOW",
            75: "HEAVY SNOW",
            77: "SNOW GRAINS",
            80: "SLIGHT RAIN SHOWERS",
            81: "MODERATE RAIN SHOWERS",
            82: "VIOLENT RAIN SHOWERS",
            85: "SLIGHT SNOW SHOWERS",
            86: "HEAVY SNOW SHOWERS",
            95: "THUNDERSTORM",
            96: "THUNDERSTORM WITH SLIGHT HAIL",
            99: "THUNDERSTORM WITH HEAVY HAIL"
        }
        return weather_codes.get(weather_code, "UNKNOWN")

    def broadcast_weather(self, city, weather_data):
        if not weather_data:
            logging.warning(f"No weather data to broadcast for {city['name']}")
            return

        try:
            current = weather_data["current"]
            
            # Create a dictionary of all OSC messages to send
            osc_messages = {
                "/CITY": city["name"],
                "/LATITUDE": float(city["lat"]),
                "/LONGITUDE": float(city["lon"]),
                "/TIME": datetime.datetime.now().isoformat(),
                "/TEMPERATURE": float(current["temperature_2m"]),
                "/WIND_SPEED": float(current["wind_speed_10m"]),
                "/HUMIDITY": float(current.get("relative_humidity_2m", 0)),
                "/TIMEZONE": str(weather_data["timezone"]),
                "/TIMEZONE_ABBREVIATION": str(time.tzname[0]),
                "/ELEVATION": float(weather_data.get("elevation", 0)),
                "/WEATHER_DESCRIPTION": self.get_weather_description(current.get("weather_code", 0))
            }
            
            # Send and log each OSC message
            for address, value in osc_messages.items():
                self.client.send_message(address, value)
                logging.info(f"Sent OSC message: {address} = {value}")
            
            logging.info(f"Successfully broadcast all weather data for {city['name']}")
        except Exception as e:
            logging.error(f"Error broadcasting weather data for {city['name']}: {e}")

    def run(self):
        logging.info("The Weather Wire is starting...")
        print("The Weather Wire is running... Press Ctrl+C to stop")
        
        while True:
            try:
                city = CITIES[self.current_city_index]
                logging.info(f"Processing city: {city['name']}")
                
                weather_data = self.get_weather_data(city)
                if weather_data:
                    self.broadcast_weather(city, weather_data)
                else:
                    logging.warning(f"No weather data received for {city['name']}")
                
                self.current_city_index = (self.current_city_index + 1) % len(CITIES)
                logging.info(f"Waiting 10 seconds before next city...")
                time.sleep(10)
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                time.sleep(10)  # Wait before retrying

if __name__ == "__main__":
    try:
        weather_wire = WeatherWire()
        weather_wire.run()
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        sys.exit(1) 