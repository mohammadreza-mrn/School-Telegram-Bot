from typing import Union

class DbModel:

    def _insert(self) -> str:
        raise NotImplementedError
    
    def _fetch(self) -> str:
        raise NotImplementedError
    
    def _fetch_by_id(self,id:int) -> str:
        raise NotImplementedError

    def _update(self,id:int,new_data:"DbModel") -> str:
        raise NotImplementedError

    def _remove(self,id:int) -> str:
        raise NotImplementedError
    
    def _fetch_last(self) -> str:
        raise NotImplementedError
    
    def _convert_to_model(self):
        raise NotImplementedError
    
    def _filter_fetch(self,**kwargs) -> str:
        raise NotImplementedError

class TokenModel(DbModel):

    table_name:str = "Token"

    def __init__(self,token:str = "",id:int = 0) -> None:
        self.__token = token
        self.__id:int = 0

    @property
    def token(self) -> str:return self.__token

    @property
    def id(self) -> int:return self.__id

    def _insert(self) -> str:
        
        sql_command:str = f"""
            INSERT INTO {self.table_name} ('Token') VALUES ('{self.token}')
        """

        return sql_command
    
    def _fetch_by_id(self,id:int) -> str:
        
        sql_command:str = f""" SELECT * FROM {self.table_name} WHERE id = {id} """
        return sql_command
    
    def _remove(self, id:int):
        
        sql_command:str = f"DELETE FROM {self.table_name} WHERE id = {id}"
        return sql_command
    
    def __last_id(self) -> str:
        sql_command:str = f"SELECT MAX(id) FROM {self.table_name}"
        return sql_command
    
    def _fetch_last(self):
        
        sql_command:str = f"SELECT * FROM {self.table_name} ORDER BY id DESC LIMIT 1"
        return sql_command
    
    def _convert_to_model(self,item) -> "TokenModel":
        
        if isinstance(item,tuple):
            return TokenModel(token=item[1],id = item[0])
        return TokenModel()
        

class AboutModel(DbModel):

    table_name:str = "About"

    def __init__(self,about:str = "",id:int = 0) -> None:
        self.__about = about
        self.__id = id

    @property
    def about(self) -> str:return self.__about

    @property
    def id(self) -> int:return self.__id


    def _insert(self):
        
        sql_command:str = f"INSERT INTO {self.table_name} ('Text') VALUES ('{self.about}');"
        return sql_command
    
    def _fetch_last(self):
        
        sql_command:str = f"SELECT * FROM {self.table_name} ORDER BY id DESC LIMIT 1"
        return sql_command
    
    def _convert_to_model(self,item) -> "AboutModel":
        
        if isinstance(item,tuple):
            return AboutModel(about=item[1],id = item[0])
        return AboutModel()
    
class ContactModel(DbModel):

    table_name:str = "Contact"

    def __init__(self,contact:str = "",id:int = 0) -> None:
        self.__contact = contact
        self.__id = id

    @property
    def contact(self) -> str:return self.__contact

    @property
    def id(self) -> int:return self.__id

    def _insert(self):
        
        sql_command:str = f"INSERT INTO {self.table_name} ('Text') VALUES ('{self.contact}')"
        return sql_command
    
    def _fetch_last(self):
        
        sql_command:str = f"SELECT * FROM {self.table_name} ORDER BY id DESC LIMIT 1"
        return sql_command
    
    def _convert_to_model(self,item) -> "ContactModel":

        if isinstance(item,tuple):
            return ContactModel(contact=item[1],id = item[0])
        return ContactModel()
    

class WelcomeTextModel(DbModel):

    table_name:str = "WelComeText"

    def __init__(self,welcome_text:str = "",id:int = 0):
        self.__welcome_text = welcome_text
        self.__id = id

    @property
    def welcome_text(self) -> str:return self.__welcome_text

    @property
    def id(self) -> int:return self.__id

    def _insert(self):
        
        sql_command:str = f"INSERT INTO {self.table_name} ('Text') VALUES ('{self.welcome_text}');"
        return sql_command
    
    def _fetch_last(self):
        
        sql_command:str = f"SELECT * FROM {self.table_name} ORDER BY id DESC LIMIT 1"
        return sql_command
    
    def _convert_to_model(self,item) -> "WelcomeTextModel":
        if isinstance(item,tuple):
            return WelcomeTextModel(welcome_text=item[1],id = item[0])
        return WelcomeTextModel()
    

class CourcesModel(DbModel):

    table_name:str = "Cources"

    def __init__(self,title:str = "",time:str = "",teacher:str = "",start_time:str = "",description:str = "",id:int = 0):
        
        self.__title = title
        self.__time = time
        self.__teacher = teacher
        self.__start_time = start_time
        self.__description = description
        self.__id = id

    @property
    def title(self) -> str:return self.__title

    @property
    def time(self) -> str:return self.__time

    @property
    def teacher(self) -> str:return self.__teacher

    @property
    def start_time(self) -> str:return self.__start_time

    @property
    def description(self) -> str:return self.__description

    @property
    def id(self) -> int:return self.__id

    def _fetch(self):
        
        sql_command:str = f"SELECT * FROM {self.table_name};"
        return sql_command
    
    def _fetch_by_id(self, id:int):
        
        sql_command:str = f"SELECT * FROM {self.table_name} WHERE id = {id};"
        return sql_command

    def _insert(self) -> str:
        
        sql_command:str = f"INSERT INTO {self.table_name} ('Title','Time','Teacher','StartTime','Description') VALUES ('{self.title}','{self.time}','{self.teacher}','{self.start_time}','{self.description}');"
        return sql_command
    
    def _remove(self, id:int) -> str:
        
        sql_command:str = f"DELETE FROM {self.table_name} WHERE id = {id};"
        return sql_command
    
    def _convert_to_model(self,item:Union[tuple,list[tuple]]) -> Union["CourcesModel",list["CourcesModel"]]:
        
        if isinstance(item,tuple):
            return CourcesModel(title=item[1],time=item[2],teacher=item[3],start_time=item[4],description=item[5],id = item[0])
        elif isinstance(item,list):
            return [CourcesModel(title=i[1],time=i[2],teacher=i[3],start_time=i[4],description=i[5],id = i[0]) for i in item]
        
    def _update(self, id:int, new_data:"CourcesModel") -> str:

        sql_command = f"UPDATE {self.table_name} SET 'Title' = '{new_data.title}','Time' = '{new_data.time}','Teacher'='{new_data.teacher}','StartTime'='{new_data.start_time}','Description'='{new_data.description}' WHERE id = {id};"
        return sql_command
        

class ProxyModel(DbModel):

    table_name:str = "Proxy"

    def __init__(self,proxy:str = "",id:int = 0) -> None:
        self.__proxy = proxy
        self.__id = id

    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def proxy(self) -> str:
        return self.__proxy
    
    def _fetch_last(self):
        
        sql_command:str = f"SELECT * FROM {self.table_name} ORDER BY id DESC LIMIT 1"
        return sql_command

    def _convert_to_model(self,item) -> "ProxyModel":
        
        if isinstance(item,tuple):
            return ProxyModel(proxy=item[1],id = item[0])
        
    def _insert(self) -> str:
        
        sql_command:str = f"INSERT INTO {self.table_name} ('Proxy') VALUES ('{self.proxy}');"
        return sql_command
    
class TelegramUserModel(DbModel):

    table_name:str = "TelegramUser"

    def __init__(self,user_id:str = "",first_name:str = "",last_name:str = "",username:str = "",language_code:str = "",id:int = 0) -> None:
        
        self.__user_id = user_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__username = username
        self.__language_code = ""
        self.__id = id

    @property
    def user_id(self) -> str:
        return self.__user_id
    
    @property
    def first_name(self) -> str:
        return self.__first_name
    
    @property
    def last_name(self) -> str:
        return self.__last_name
    
    @property
    def username(self) -> str:
        return self.__username
    
    @property
    def language_code(self) -> str:
        return self.__language_code
    
    @property
    def id(self) -> int:
        return self.__id
    
    def _insert(self) -> str:
        
        sql_command:str = f"INSERT INTO {self.table_name} ('UserId','FirstName','LastName','UserName','LanguageCode') VALUES ('{self.user_id}','{self.first_name}','{self.last_name}','{self.username}','{self.language_code}');"
        return sql_command
    
    def check_repeted_item(self,user_id:str) -> bool:

        sql_command:str = f"SELECT UserId from {self.table_name} WHERE EXISTS (SELECT UserId FROM {self.table_name} WHERE UserId = '{user_id}');"
        return sql_command
    
    def _fetch(self) -> str:

        sql_command:str = f"SELECT * FROM {self.table_name};"
        return sql_command
    
    def _convert_to_model(self,item) -> Union["TelegramUserModel",list["TelegramUserModel"]]:
        
        if isinstance(item,tuple):
            return TelegramUserModel(
                user_id=item[1],
                first_name=item[2],
                last_name=item[3],
                username=item[4],
                language_code=item[5],
                id = item[0]
            )
        elif isinstance(item,list):
            
            return [TelegramUserModel(
                user_id=i[1],
                first_name=i[2],
                last_name=i[3],
                username=i[4],
                language_code=i[5],
                id = i[0]
            ) for i in item]
        

class BotMessagesTiming(DbModel):

    table_name:str = "BotMessagesTiming"

    def __init__(self,time:str = "",date:str = "",message:str = "",done:int = 0,recivers:str = "",id:int = 0) -> None:
        self.__time:str = time
        self.__date:str = date
        self.__message:str = message
        self.__done:int = done
        self.__recivers:str = recivers
        self.__id = id


    @property
    def time(self) -> str:
        return self.__time
    
    @property
    def date(self) -> str:
        return self.__date
    
    @property
    def message(self) -> str:
        return self.__message
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def done(self) -> int:
        """ its integer value and 1 means True and 0 means False """
        return self.__done
    
    @property
    def recivers(self) -> str:
        return self.__recivers

    def _insert(self) -> str:

        sql_command:str = f"INSERT INTO {self.table_name} ('Time','Date','Message','Done','Recivers') VALUES ('{self.time}','{self.date}','{self.message}','{self.done}','{self.recivers}');"
        return sql_command
    
    def _fetch(self) -> str:
        
        sql_command:str = f"SELECT * FROM {self.table_name};"
        return sql_command
    
    def _convert_to_model(self,item) -> Union["BotMessagesTiming",list["BotMessagesTiming"]]:
        
        if isinstance(item,tuple):
            return BotMessagesTiming(
                id = item[0],
                time = item[1],
                date = item[2],
                message = item[3],
                done=item[4],
                recivers=item[5].split("-")
            )
        
        elif isinstance(item,list):

            return [
                BotMessagesTiming(
                    id = i[0],
                    time = i[1],
                    date = i[2],
                    message = i[3],
                    done = i[4],
                    recivers = i[5].split("-")
                ) for i in item
            ]
    def _filter_fetch(self, **kwargs):
        
        sql_command:str = f"SELECT * FROM {self.table_name} WHERE "

        for key,value in kwargs.items():
            if isinstance(value,int):
                sql_command += f"{key} = {value} AND "
            elif isinstance(value,str):
                sql_command += f"{key} = '{value}' AND "

        if sql_command.endswith("AND "):
            sql_command = sql_command[:len(sql_command) - 4]
            sql_command.strip()

        sql_command += ";"
        return sql_command
    
    def _remove(self, id:int) -> str:
        
        sql_command:str = f"DELETE FROM {self.table_name} WHERE id = {id};"
        return sql_command