
from ingestion import WeatherIngestion
from transformation import WeatherTransformation
from loading import WeatherLoader
from pathlib import Path


def update_pipeline():
    print("Joe Weather Data Pipeline")
    print("Station: Belleville, Ontario")

    # Find the historical CSV file
    csv_files = list(Path(__file__).parent.glob("en_climate_daily_*.csv"))

    if not csv_files:
        print("Error: ECCC CSV file not found.")
        return

    # Step 1: Ingestion
    ingestion = WeatherIngestion()
    historical_data = ingestion.load_historical_data(csv_files[0])

    print("\nFirst 5 rows of historical data:")
    print(historical_data.head())

    # Step 2: Transformation
    transformation = WeatherTransformation()

    september_data = transformation.filter_historical_data(
        historical_data
    )

    print("\nSeptember 2026 historical data:")
    print(september_data[["Date/Time", "Year", "Month", "Day"]].head())

    print("Total September records:", len(september_data))
    
    # Step 3: Standardize historical weather data
    standardized_historical = transformation.standardize_historical_data(
        september_data
    )

    print("\nStandardized historical data:")
    print(standardized_historical.head())

    print("\nStandardized column names:")
    print(standardized_historical.columns.tolist())
    print("\nHistorical weather columns:")
    print(september_data.columns.tolist())
# Step 4: Fetch Open-Meteo forecast data
    forecast_data = ingestion.fetch_forecast_data()

    print("\nOpen-Meteo forecast information:")
    print("Timezone:", forecast_data["timezone"])
    print("Number of hourly records:", len(forecast_data["hourly"]["time"]))
    print("First forecast date:", forecast_data["hourly"]["time"][0])

    # Step 4: Transform hourly forecast into daily records
    daily_forecast = transformation.transform_forecast_data(
        forecast_data
    )

    print("\nDaily forecast data:")
    print(daily_forecast.head())

    print("Total forecast days:", len(daily_forecast))
    
    # Step 5: Standardize forecast data
    standardized_forecast = transformation.standardize_forecast_data(
        daily_forecast
    )

    print("\nStandardized forecast data:")
    print(standardized_forecast.head())

    print("\nForecast column names:")
    print(standardized_forecast.columns.tolist())

    # Step 6: Combine historical and forecast data
    loader = WeatherLoader()

    combined_data = loader.combine_weather_data(
        standardized_historical,
        standardized_forecast
    )

    print("\nCombined weather data:")
    print(combined_data.head())

    print("\nLast 5 records:")
    print(combined_data.tail())

    print("\nTotal combined records:", len(combined_data))

    print("\nRecords by source:")
    print(combined_data["source_type"].value_counts())

    # Step 7: Save the integrated weather data
    output_path = Path(__file__).parent / "Joe_Integrated_Weather_Data.csv"

    loader.save_weather_data(
        combined_data,
        output_path
    )

    # Step 8: Validate the integrated weather data
    loader.validate_weather_data(combined_data)

    print("\nWeather pipeline completed successfully!")



if __name__ == "__main__":
    update_pipeline()