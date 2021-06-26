import sys, os
from sqlalchemy import Column, String, Integer
import sys,os
from src.data_access.postgres import declarative_base as base

class DaoSealCoin(base):

    __tablename__ = 'SealCoin'

    audience = Column(String, primary_key=True)
    coin = Column(Integer)
