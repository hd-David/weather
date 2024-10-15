from sqlalchemy import Table, Column,Integer, String, MetaData,Float, DateTime, create_engine, Text
from datetime import datetime
from sqlalchemy.orm import  DeclarativeBase, Session
import sqlite3



class Base(DeclarativeBase):
    pass


class SearchHistory(Base):
    __tablename__ = 'search'
    
    id = Column(Integer, primary_key=True)
    city = Column(String(64))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    weather_data = Column(Text(1000), nullable=False)



# database connection
def dbconnect():
   
    engine = create_engine('sqlite:///weather.db')
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        return session
