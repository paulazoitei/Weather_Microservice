
from sqlalchemy import func, DateTime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base=declarative_base()
engine=create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session=sessionmaker(bind=engine)

class Storage(Base):
    __tablename__='weather_data'

    id=Column(Integer,primary_key=True)
    city_name=Column(String(50),nullable=False)
    temperature=Column(Float,nullable=False)
    description=Column(String(50),nullable=False)
    humidity=Column(Integer,nullable=False)
    wind_speed=Column(Float,nullable=False)
    data_created=Column(DateTime,nullable=False)


def save_weather_data(city_name,temperature,description,humidity,wind_speed,data_created):
    session=Session()
    entry=Storage(
        city_name=city_name,
        temperature=temperature,
        description=description,
        humidity=humidity,
        wind_speed=wind_speed,
        data_created=data_created

    )
    session.add(entry)
    session.commit()
    session.close()


