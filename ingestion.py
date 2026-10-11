
import pandas as pd
import requests


class WeatherIngestion:

    def load_historical_data(self, csv_path):
        """Load ECCC historical weather data."""
        data = pd.read_csv(csv_path, encoding="utf-8-sig")
        print("Historical data loaded successfully.")
        return data

    def fetch_forecast_data(self):
        """Fetch 16-day weather forecast from Open-Meteo."""
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": 44.15,
            "longitude": -77.39,
            "hourly": [
                "temperature_2m",
                "precipitation",
                "relative_humidity_2m"
            ],
            "forecast_days": 16,
            "timezone": "auto"
        }

        response = requests.get(
            url, params=params, timeout=30
        )
        response.raise_for_status()

        forecast = response.json()
        print("Forecast data fetched successfully.")

        return forecast
