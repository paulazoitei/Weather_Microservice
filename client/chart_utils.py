from datetime import datetime
from server.storage import Session, Storage
from sqlalchemy import and_
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
class ChartUtils:
    @staticmethod
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
    @staticmethod
    def create_plot(city_name, dates, temperatures):
        try:
            fig, ax = plt.subplots(figsize=(9, 6))
            ax.set_xlabel("Dates from 1 to 5 august", fontsize=12)
            ax.set_ylabel("Temperatures")
            ax.set_title(f"Temperature fluctuation chart for {city_name}")
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

            ax.plot(dates, temperatures, linestyle='--', marker='o', color='red')
            plt.show()
        except Exception as e:
            print(f" Error generating chart:{e}")