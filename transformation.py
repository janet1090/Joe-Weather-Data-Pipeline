
import pandas as pd


class WeatherTransformation:

    def filter_historical_data(self, data):
        """Select September 2026 historical records."""

        september_data = data[
            (data["Year"] == 2026) &
            (data["Month"] == 9)
        ].copy()

        print("September 2026 data filtered successfully.")

        return september_data

    def standardize_forecast_data(self, daily_forecast):
        """Prepare forecast records for the flat data model."""

        forecast = daily_forecast.rename(columns={
            "temperature_2m": "temperature",
            "relative_humidity_2m": "humidity"
        }).copy()

        forecast["station_name"] = "BELLEVILLE"
        forecast["latitude"] = 44.15
        forecast["longitude"] = -77.39
        forecast["source_type"] = "forecast"

        # Match the historical column order
        forecast = forecast[[
            "date",
            "station_name",
            "latitude",
            "longitude",
            "temperature",
            "precipitation",
            "humidity",
            "source_type"
        ]]

        print("Forecast data standardized successfully.")

        return forecast

    def standardize_historical_data(self, september_data):
        """Prepare historical records for the flat data model."""

        historical = september_data[[
            "Date/Time",
            "Station Name",
            "Latitude (y)",
            "Longitude (x)",
            "Mean Temp (°C)",
            "Total Precip (mm)"
        ]].copy()

        historical = historical.rename(columns={
            "Date/Time": "date",
            "Station Name": "station_name",
            "Latitude (y)": "latitude",
            "Longitude (x)": "longitude",
            "Mean Temp (°C)": "temperature",
            "Total Precip (mm)": "precipitation"
        })

        historical["date"] = pd.to_datetime(
            historical["date"]
        ).dt.date

        historical["humidity"] = pd.NA
        historical["source_type"] = "historical"

        print("Historical data standardized successfully.")

        return historical

    def transform_forecast_data(self, forecast_data):
        """Convert Open-Meteo hourly forecast data into daily data."""

        # Convert the hourly forecast JSON into a pandas DataFrame
        hourly_data = pd.DataFrame(forecast_data["hourly"])

        # Convert timestamps into dates
        hourly_data["date"] = pd.to_datetime(
            hourly_data["time"]
        ).dt.date

        # Group the hourly records by date
        daily_data = hourly_data.groupby("date").agg({
            "temperature_2m": "mean",
            "precipitation": "sum",
            "relative_humidity_2m": "mean"
        }).reset_index()

        print("Forecast data transformed into daily records.")

        return daily_data
