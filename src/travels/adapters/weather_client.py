import logging
from datetime import date, datetime
from typing import Any, Tuple
import requests
from requests import Response

from travels.conf import conf

logger = logging.getLogger(__name__)

class WeatherClientException(Exception):
    pass

class UnAuthorizedException(WeatherClientException):
    pass

class ForecastDaysExceededException(WeatherClientException):
    pass

class WeatherClient:
    HTTP_401_UNAUTHORIZED = 401
    HTTP_200_OK = 200

    def __init__(self, requester=requests) -> None:
        self.requester = requests


    def _get(
        self,
        path:
        str,
        query_params:
        dict=None,
        headers:
        dict=None
    ) -> Response:
        """
        :param path: (str) Relative path.
        :param query_params: (dict) Dict with the query params.
        :param headers: (dict) Dict with the headers to add.
        :return: (request.Response)
        """
        query_params_str = f"?key={conf.WEATHER_KEY}"
        for key, value in query_params.items():
            query_params_str += f"&{key}={value}"

        url = f"{conf.WEATHER_BASE_URL}/{path}{query_params_str}"
        logger.info(f"GET {url}")
        response = requests.get(url=url, headers=headers)
        logger.info(f"status code response: {response.status_code}")
        if response.status_code == self.HTTP_401_UNAUTHORIZED:
            logger.error(response.content)
            raise UnAuthorizedException()

        return response

    def get_forecast_for_date(
        self, lat: str, lon: str, forecast_date: date
    ) -> dict:
        """
        Max forecast days is actually 15.
        """
        date_now = datetime.now().date()
        days_now_up_to_forecast_date = (forecast_date - date_now).days + 1
        if days_now_up_to_forecast_date >= 15:
            raise ForecastDaysExceededException()

        query_params = {
            "q": f"{lat},{lon}",
            "aqi": "no",
            "alerts": "no",
            "days": days_now_up_to_forecast_date
        }
        path = "v1/forecast.json"
        response = self._get(path=path, query_params=query_params)
        if response.status_code != self.HTTP_200_OK:
            msg = f"Body response: {response.content}"
            logger.error(msg)
            raise WeatherClientException()
        
        data = response.json()
        for forecast_day in data["forecast"]["forecastday"]:
            if forecast_day["date"] == forecast_date.strftime("%Y-%m-%d"):
                return {
                    "max_temp": forecast_day["day"].get("maxtemp_c"),
                    "min_temp": forecast_day["day"].get("mintemp_c"),
                    "avg_temp": forecast_day["day"].get("avgtemp_f"),
                    "daily_chance_of_rain": forecast_day["day"].get("daily_chance_of_rain")
                }
            