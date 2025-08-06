import os
import sys
from datetime import datetime
from sqlalchemy import and_

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from protos import weather_pb2_grpc,weather_pb2
import time
import grpc
import matplotlib.pyplot as plt
import pandas as pd
from server.storage import Session, Storage
import matplotlib.dates as mdates

def get_temperature_and_dates(city_name):
    try:
        start_date = datetime(2025, 8, 1)
        end_date = datetime(2025, 8, 5, 23, 59, 59)
        session = Session()
        query = session.query(Storage.temperature, Storage.data_created).filter(
            and_(
                Storage.city_name == city_name,
                Storage.data_created >= start_date,
                Storage.data_created <= end_date
            )
        )
        results = query.all()
        session.close()

        temperatures = []
        dates = []
        for temp, date in results:
            temperatures.append(temp)
            dates.append(date)

        return dates, temperatures

    except Exception as e:
        print(f" Error fetching data from DB: {e}")
        return [], []

def create_plot(city_name,dates,temperatures):
    try:
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.set_xlabel("Dates from 1 to 5 august", fontsize=12)
        ax.set_ylabel("Temperatures")
        ax.set_title(f"Temperature fluctuation chart for {city_name}")
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

        ax.plot(dates, temperatures, linestyle='--', marker='o', color='red')
        plt.show()
    except Exception as e:
        print(f" Error generating chart:{e}")


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

                dates,temps=get_temperature_and_dates(city)

                if not dates:
                    print(f"No data found for {city} between 1-5 August.")
                    print()
                    continue

                create_plot(city, dates, temps)


            else:
                print(" Please put a valid command on CLI (1,2 or 3)")
                print()



if __name__=="__main__":
    run()

