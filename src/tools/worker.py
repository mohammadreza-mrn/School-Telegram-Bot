import asyncio
from typing import Optional
from datetime import datetime

from telegram.error import NetworkError,InvalidToken

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget

from src.telegram.handler import BotManager

from models.db_config import InteractDB
from models.models import TelegramUserModel,BotMessagesTiming

from .widget_helpers import DateTimeConverter

class BotWorker(QThread):

    error_occured = pyqtSignal(Exception,str)
    connection_success = pyqtSignal(str)
    new_message = pyqtSignal(list)

    def __init__(self, token:str,proxy:Optional[str] = None,parent:Optional[QWidget] = None,interact_db:Optional[InteractDB] = None):
        self.token:str = token
        self.__interact_db = interact_db
        self.__proxy:str = proxy
        super().__init__(parent)


    def run(self):
        bot_manager = BotManager(self.token,self.__proxy)
        try:
            self.connection_success.emit("اتصال برقرار است")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(bot_manager.app.run_polling())

        except NetworkError as network_ex:
            del bot_manager
            self.error_occured.emit(network_ex,"خطا در اتصال به تلگرام")

        except InvalidToken as invalidtoken_ex:
            del bot_manager
            self.error_occured.emit(invalidtoken_ex,"توکن وارد شده معتبر نیست")
        

class MessageQueueSendTimeWorker(QThread):

    message_sent = pyqtSignal(str,int)
    error_recived = pyqtSignal(str)

    messages_list:list[BotMessagesTiming] = None

    def __init__(self,token:str = "",proxy:str = "",parent:Optional[QWidget] = None) -> None:
        
        self.__token:str = token
        self.__proxy:str = proxy
        super().__init__(parent)

    def run(self):
        
        while True:
            now = datetime.now()
            for message in self.messages_list:

                _datetime:str = f"{message.date} {message.time}"
                _datetime:datetime = datetime.strptime(_datetime,"%Y/%m/%d %H:%M")
                if self.__check_time_equal(now,_datetime):
                    try:
                        BotManager.send_many_messages(self.__token,message.recivers,message.message)
                        self.messages_list.remove(message)
                        self.message_sent.emit("یک پیام ارسال شد",message.id)
                    except NetworkError as e:
                        print(e)
                        self.error_recived.emit("خطا در ارسال پیام")

    def __check_time_equal(self,first_time:datetime,second_time:datetime) -> bool:
        
        return DateTimeConverter.check_time_equals(first_time,second_time)