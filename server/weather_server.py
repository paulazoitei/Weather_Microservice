from concurrent import futures
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import grpc
from protos import weather_pb2, weather_pb2_grpc
import requests


class GreeterServicer(weather_pb2_grpc.GreeterServicer):
    def Give_Weather_Details(self,request,context):
        base_url="http://api.openweathermap.org/data/2.5/weather?"
        api_key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api_key'))
        with open(api_key_path, 'r') as f:
            api_key = f.read().strip()
        city=f"{request.city_name}"
        url=base_url+"appid=" + api_key+"&q="+city
        response=requests.get(url).json()
        city_name=response["name"]
        temperature = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        description = response["weather"][0]["description"]
        wind_speed = response["wind"]["speed"]


        weather_response=weather_pb2.WeatherResponse(city_name=city_name,
                                                     temperature=temperature,
                                                     description=description,
                                                     humidity=humidity,
                                                     wind_speed=wind_speed)


        return weather_response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()