
import pandas as pd


class WeatherLoader:
    
    def validate_weather_data(self, combined_data):
        """Check the quality of the integrated weather data."""

        print("\nDATA VALIDATION REPORT")

        print("Total records:", len(combined_data))

        duplicates = combined_data.duplicated(
            subset=["date", "station_name", "source_type"]
        ).sum()

        print("Duplicate records:", duplicates)

        print("\nMissing values:")
        print(combined_data.isnull().sum())

        invalid_dates = pd.to_datetime(
            combined_data["date"], errors="coerce"
        ).isna().sum()

        print("\nInvalid dates:", invalid_dates)

        print("Data validation completed.")

    def save_weather_data(self, combined_data, output_path):
        """Save the integrated weather data to a CSV file."""

        combined_data.to_csv(output_path, index=False)

        print("Integrated weather data saved successfully.")
        print("Output file:", output_path)

    def combine_weather_data(self, historical, forecast):
        """Combine historical and forecast data into one flat table."""

        combined_data = pd.concat(
            [historical, forecast],
            ignore_index=True
        )

        # Remove duplicate dates within each source
        combined_data = combined_data.drop_duplicates(
            subset=["date", "station_name", "source_type"],
            keep="last"
        )

        # Sort the records by date
        combined_data = combined_data.sort_values(
            by="date"
        ).reset_index(drop=True)

        print("Historical and forecast data combined successfully.")

        return combined_data
