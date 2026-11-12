# Joe Weather Data Pipeline

A COMP248 prototype that combines historical weather observations from Environment and Climate Change Canada (ECCC) with forecasts from the Open-Meteo API for Belleville, Ontario.

## What it does

- Reads ECCC daily historical weather data from a CSV file.
- Retrieves hourly forecast data from Open-Meteo.
- Aggregates hourly forecasts into daily temperature, precipitation, and humidity values.
- Standardizes and combines both datasets into one CSV.
- Checks for duplicate records, invalid dates, and missing values while preserving unavailable measurements.

## Project structure

- `ingestion.py` — reads historical data and retrieves forecasts.
- `transformation.py` — filters, aggregates, and standardizes the data.
- `loading.py` — combines, validates, and saves the dataset.
- `main.py` — runs the pipeline.

## Run the pipeline

Install the required Python packages:

```bash
pip install pandas requests
```

From the project folder, run:

```bash
python main.py
```

The output is saved as `Joe_Integrated_Weather_Data.csv`. The prototype is run manually; scheduled updates and a prediction model are outside its current scope.

## Sample run

The report records 30 historical records and 16 forecast records: 46 total, with no duplicates or invalid dates. Missing historical measurements were preserved.

## Design report and walkthrough

- [COMP248 system design report](Adetoun_Janet_Adewusi_COMP248_Assignment1_Report.pdf)
- [Project explanation video](video2029419206.mp4)
