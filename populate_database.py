from datetime import datetime

import random

from server.storage import save_weather_data

import random
from datetime import datetime
from server.storage import save_weather_data

cities = ["London", "Paris", "Berlin", "Madrid", "Rome"]

for city in cities:
    for day in range(1, 6):
        temperature = round(random.uniform(20, 35), 2)
        humidity = random.randint(40, 90)
        wind_speed = round(random.uniform(1, 5), 2)
        description = "test data"
        data_created = datetime(2025, 8, day)

        try:
            save_weather_data(
                city_name=city,
                temperature=temperature,
                description=description,
                humidity=humidity,
                wind_speed=wind_speed,
                data_created=data_created
            )
            print(f" Added: {city} | {data_created.date()} | {temperature}°C")
        except Exception as e:
            print(f" Failed to insert {city} on {data_created.date()}: {e}")
