from datetime import datetime
from server.storage import Session, Storage
from sqlalchemy import and_


class TemperaturesProcess:
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