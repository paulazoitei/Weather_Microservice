import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from protos import weather_pb2_grpc,weather_pb2
import time
import grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub=weather_pb2_grpc.GreeterStub(channel)
        while True:
            rpc_call=input("Enter city name: ")


            weather_request=weather_pb2.WeatherRequest(city_name=f"{rpc_call}")
            weather_response=stub.Give_Weather_Details(weather_request)

            print(weather_response)

            if rpc_call=="exit":
                break

if __name__=="__main__":
    run()

