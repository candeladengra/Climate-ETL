import openmeteo_requests
import pandas as pd
import psycopg2
import requests_cache
from retry_requests import retry
from configparser import ConfigParser
from datetime import date


def read_credentials(config_file, section):
    config = ConfigParser()
    config.read(config_file)
    credentials = dict(config[section])
    return credentials


cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": [
        -34.61315,
        -31.4135,
        -32.94682,
        -32.89084,
        -26.82414,
        -34.92145,
        -38.00042,
        -24.7859,
        -31.64881,
        -31.5375,
        -27.46056,
        -27.79511,
        -27.36708,
        -24.19457,
        -38.71959,
        -31.73271,
        -34.66627,
        -34.51541,
        -34.72904,
        -34.45866,
    ],
    "longitude": [
        -58.37723,
        -64.18105,
        -60.63932,
        -68.82717,
        -65.2226,
        -57.95453,
        -57.5562,
        -65.41166,
        -60.70868,
        -68.53639,
        -58.98389,
        -64.26149,
        -55.89608,
        -65.29712,
        -62.27243,
        -60.52897,
        -58.72927,
        -58.76813,
        -58.26374,
        -58.9142,
    ],
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "wind_speed_10m_max",
    ],
}
responses = openmeteo.weather_api(url, params=params)

daily_data = {}

for location in responses:
    daily = location.Daily()
    daily_data[location.LocationId()] = {
        "daily_temperature_2m_max": daily.Variables(0).ValuesAsNumpy(),
        "daily_temperature_2m_min": daily.Variables(1).ValuesAsNumpy(),
        "daily_wind_speed_10m_max": daily.Variables(2).ValuesAsNumpy(),
    }

daily_data_list = []

date_range = pd.date_range(
    start=pd.to_datetime(daily.Time(), unit="s"),
    end=pd.to_datetime(daily.TimeEnd(), unit="s"),
    freq=pd.Timedelta(seconds=daily.Interval()),
    inclusive="left",
)

for location_id, location_data in daily_data.items():
    for date in date_range:
        daily_temperature_2m_max = location_data["daily_temperature_2m_max"]
        daily_temperature_2m_min = location_data["daily_temperature_2m_min"]
        daily_wind_speed_10m_max = location_data["daily_wind_speed_10m_max"]

        daily_data_dict = {
            "predicted_date": date,
            "prediction_date": date.today(),
            "locationId": location_id + 1,
            "temperature_2m_max": daily_temperature_2m_max[date_range.get_loc(date)],
            "temperature_2m_min": daily_temperature_2m_min[date_range.get_loc(date)],
            "wind_speed_max": daily_wind_speed_10m_max[date_range.get_loc(date)],
        }
        daily_data_list.append(daily_data_dict)


def connect_to_database():
    credentials = read_credentials("config/pipeline.conf", "redshift")
    conn = psycopg2.connect(
        user=credentials["db_user"],
        dbname=credentials["db_name"],
        password=credentials["db_password"],
        host=credentials["host"],
        port=credentials["db_port"],
    )
    return conn


def insert_forecast_data():
    conn = connect_to_database()
    insert_query = """
    INSERT INTO forecast (date, prediction_date, locationId, max_temperature, min_temperature, precipitation_probability_max)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur = conn.cursor()

    data_values = [
        (
            data["predicted_date"],
            data["prediction_date"],
            data["locationId"],
            float(data["temperature_2m_max"]),
            float(data["temperature_2m_min"]),
            float(data["wind_speed_max"]),
        )
        for data in daily_data_list
    ]

    cur.executemany(insert_query, data_values)

    conn.commit()
    cur.close()
    conn.close()
