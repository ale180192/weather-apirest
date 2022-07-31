from os.path import dirname as up

dir = up(up(__file__))

BASE_DIR =  up(up(__file__))
PARENT_BASE_DIR = up(BASE_DIR)

# REDIS
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# WEATHER
WEATHER_KEY = "0c93c3e831574473aaa233556220208"
WEATHER_BASE_URL = "https://api.weatherapi.com"
