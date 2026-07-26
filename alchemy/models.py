from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    )
from sqlalchemy.orm import declarative_base

"""
                #databse_type# + #db_driver#://#username#:#password#@#host#:#post#/#db_name#
"""
CONNECTION_STRING = 'postgresql+psycopg2://postgres:password@localhost:5432/exam_prep'

engine = create_engine(CONNECTION_STRING)

Base = declarative_base()

class Worker(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False, default='Mitko')
    last_name = Column(String(30), nullable=False, default='Petkov')
    age = Column(Integer)
    salary = Column(Integer)
