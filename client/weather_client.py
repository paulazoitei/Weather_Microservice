import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from protos import weather_pb2_grpc,weather_pb2
import grpc

from temperatures_chart import TemperaturesChart
from temperatures_process import  TemperaturesProcess

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        try:
            stub=weather_pb2_grpc.GreeterStub(channel)
        except Exception as e:
            print(f"The RPC call to the server failed:{e}")
            return
        while True:

            rpc_call = input(
                "Please select the option you want to use:\n"
                "  1. View weather details about a city\n"
                "  2. View a temperature fluctuation chart for London,Paris,Berlin,Madrid,Rome from 1 august to 5 august.\n"
                "  3. Exit CLI\n"
                "Your choice: "

            )
            print()


            if rpc_call=="3":
                break

            elif rpc_call=="1":
                town = input("Enter a city name: ")
                print()
                weather_request=weather_pb2.WeatherRequest(city_name=f"{town}")
                try:
                     weather_response=stub.Give_Weather_Details(weather_request)
                except Exception as e:
                    print(f"The city with name {town} does not exist")
                    print()
                    continue
                print(weather_response)
            elif rpc_call=="2":
                city=input("Enter city name: ")
                print()
                valid_cities = ["London", "Madrid", "Paris", "Rome", "Berlin"]
                if city not in valid_cities:
                    print("Please choose one of the supported cities.")
                    print()
                    continue

                dates,temps=TemperaturesProcess.get_temperature_and_dates(city)

                if not dates:
                    print(f"No data found for {city} between 1-5 August.")
                    print()
                    continue

                TemperaturesChart.create_plot(city, dates, temps)


            else:
                print(" Please put a valid command on CLI (1,2 or 3)")
                print()



if __name__=="__main__":
    run()

