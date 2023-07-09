import os
from sqlalchemy import create_engine
from helper.singleton import Singleton
from sqlalchemy.orm import sessionmaker

class Postgres(metaclass=Singleton):
    def __init__(self) -> None:
        self.__username = os.getenv('POSTGRES_USER')
        self.__password = os.getenv('POSTGRES_PASSWORD')
        self.__host = os.getenv('POSTGRES_HOST')
        self.__database = os.getenv('POSTGRES_DB')
        self.__engine = None
        self.__connection = None

    def createEngine(self):
        connection_string = f'postgresql+psycopg2://{self.__username}:{self.__password}@{self.__host}/{self.__database}'
        self.__engine = create_engine(connection_string)
        self.__session = sessionmaker(self.__engine)
        return self

    def createConnection(self):
        self.__connection = self.__engine.connect()
        return self

    @property
    def engine(self):
        return self.__engine

    @property
    def connection(self):
        return self.__connection

    @property
    def session(self):
        return self.__session

    def __del__(self):
        if self.__connection != None:
            self.__connection.close()