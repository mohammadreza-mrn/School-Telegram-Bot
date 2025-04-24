import os
import sqlite3
from typing import Callable

from .models import DbModel

class DatabaseConfig:

    def __init__(self,db_name:str) -> None:

        self.__db_name:str = db_name
        self.create_database()

    def connect(self) -> sqlite3.Connection:

        connection = sqlite3.connect(self.__db_name)
        self.create_tables(connection)
        return connection

    def create_database(self) -> None:
        
        if not os.path.isfile(self.__db_name):
            file = open(self.__db_name,"x")
            file.close()


    def create_tables(self,connection:sqlite3.Connection) -> None:


        tables_list = [
            self.token_table,
            self.about_table,
            self.contact_table,
            self.welcome_text_table,
            self.cources_list_table,
            self.proxy_model,
            self.telegram_user_model,
            self.bot_messages_timing,
        ]

        for table in tables_list:
            connection.execute(table)



    @property
    def token_table(self) -> str:

        sql_command:str = """
            CREATE TABLE IF NOT EXISTS Token (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Token' NNARCHAR(130) NOT NULL
            );
        """

        return sql_command
    
    # @property
    # def cources_table(self) -> str:

    #     sql_command:str = """
    #         CREATE TABLE IF NOT EXISTS Cources (
    #             'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    #             'Title' NVARCHAR(150) NOT NULL,
    #             'Time' NVARCHAR(100) NOT NULL,
    #             'Teacher' NVARCHAR(100),
    #             'Description' NVARCHAR(500)
    #         );
    #     """

    #     return sql_command
    
    @property
    def about_table(self) -> str:

        sql_command:str = f"""
            CREATE TABLE IF NOT EXISTS About (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Text' NVARCHAR NOT NULL
            );
        """
        return sql_command
    
    @property
    def contact_table(self) -> str:

        sql_command:str = f""" 
            CREATE TABLE IF NOT EXISTS Contact (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Text' NVARCHAR NOT NULL
            );
        """
        return sql_command
    
    @property
    def welcome_text_table(self) -> str:

        sql_command:str = f"""
            CREATE TABLE IF NOT EXISTS WelComeText (
              'id' INTEGER PRIMARY KEY AUTOINCREMENT,
              'Text' NVARCHAR NOT NULL
            )
        """
        return sql_command
    
    @property
    def cources_list_table(self) -> str:

        sql_command:str = f""" 
            CREATE TABLE IF NOT EXISTS Cources (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Title' NVARCHAR(200) NOT NULL,
                'Time' NVARCHAR(100) NOT NULL,
                'Teacher' NVARCHAR(100) NOT NULL,
                'StartTime' NVARCHAR(100),
                'Description' NVARCHAR
            );
        """
        return sql_command

    @property
    def proxy_model(self) -> str:

        sql_command:str = f""" 
            CREATE TABLE IF NOT EXISTS Proxy (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Proxy' NVARCHAR(200) NOT NULL
            );
        """
        return sql_command
    
    @property
    def telegram_user_model(self) -> str:

        sql_command:str = f"""
            CREATE TABLE IF NOT EXISTS TelegramUser (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'UserId' NVARCHAR(50) NOT NULL,
                'FirstName' NVARCHAR(100) NOT NULL,
                'LastName' NVARCHAR(100) NOT NULL,
                'UserName' NVARCHAR(100),
                'LanguageCode' NVARCHAR(10)
            );
        """
        return sql_command
    
    @property
    def bot_messages_timing(self) -> str:

        sql_command:str = f""" 
            CREATE TABLE IF NOT EXISTS BotMessagesTiming (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Time' NVARCHAR(100) NOT NULL,
                'Date' NVARCHAR(100) NOT NULL,
                'Message' NVARCHAR NOT NULL,
                'Done' INTEGER NOT NULL DEFAULT 0,
                'Recivers' NVARCHAR NOT NULL
            );
        """
        return sql_command
    
    
class InteractDB:

    def __init__(self,connection:sqlite3.Connection):
        
        self.__connection = connection

    def fetch_all(self,model:DbModel):
        
        cursor = self.__connection.cursor()
        cursor.execute(model._fetch())
        all_items = cursor.fetchall()
        return model._convert_to_model(all_items)

    def fetch_by_id(self,model:DbModel):
        
        cursor = self.__connection.cursor()
        cursor.execute(model._fetch_by_id(model.id))
        found_item = cursor.fetchone()
        return model._convert_to_model(found_item)

    def insert(self,model:DbModel):
        self.__connection.execute(model._insert())
        self.__connection.commit()
        
    def fetch_last(self,model:DbModel) -> DbModel:

        cursor = self.__connection.cursor()
        cursor.execute(model._fetch_last())
        last_item = cursor.fetchone()
        return model._convert_to_model(last_item)
    
    def check_exists(self,function:Callable,**kwargs) -> bool:
        
        sql_command = function(**kwargs)
        cursor = self.__connection.cursor()
        cursor.execute(sql_command)
        item = cursor.fetchone()
        return bool(item)
    
    def remove(self,model:DbModel,id:int) -> bool:

        try:
            self.__connection.execute(model._remove(id))
            self.__connection.commit()
            return True
        except:
            return False
        
    def update(self,model:DbModel,id:int) -> bool:

        try:
            self.__connection.execute(model._update(id,model))
            self.__connection.commit()
            return True
        except Exception as e:
            return False

    def filter_fetch(self,model:DbModel,**kwargs):

        cursor = self.__connection.cursor()
        cursor.execute(model._filter_fetch(**kwargs))
        item = cursor.fetchall()
        return model._convert_to_model(item)
        