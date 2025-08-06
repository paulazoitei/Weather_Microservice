from concurrent import futures
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import grpc
from protos import weather_pb2, weather_pb2_grpc
import requests
from server.storage import save_weather_data


class GreeterServicer(weather_pb2_grpc.GreeterServicer):
    def Give_Weather_Details(self, request, context):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        api_key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api_key'))


        try:
            with open(api_key_path, 'r') as f:
                api_key = f.read().strip()
        except (FileNotFoundError, PermissionError) as e:
            print(f"API Key error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Server configuration error")
            return weather_pb2.WeatherResponse()

        city = request.city_name
        url = f"{base_url}q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200 or "main" not in data:
                raise ValueError(f"City not found or invalid response: {data}")


            city_name = data["name"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]
            data_created=datetime.now()


            try:
                save_weather_data(city_name, temperature, description, humidity, wind_speed,data_created)
            except Exception as e:
                print(f"Error saving to database: {e}")

            return weather_pb2.WeatherResponse(
                city_name=city_name,
                temperature=temperature,
                description=description,
                humidity=humidity,
                wind_speed=wind_speed,
                data_created=data_created.isoformat()
            )

        except Exception as e:
            print(f"Error getting weather data: {e}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Could not retrieve data for city: {city}")
            return weather_pb2.WeatherResponse()



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()