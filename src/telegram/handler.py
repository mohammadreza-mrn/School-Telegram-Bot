
import time
import httpx
import asyncio
from typing import Optional,Union

from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,ContextTypes,filters
from telegram import Update,InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton
from telegram.error import NetworkError,Forbidden
from telegram import Bot

from models.db_config import DatabaseConfig,InteractDB
from models.models import (AboutModel
                           ,ContactModel,
                           WelcomeTextModel,
                           TelegramUserModel,CourcesModel)


class MyCommandHandler:

    about_us_text:str = "درباره ما"
    contact_us_text:str = "تماس با ما"
    cources_list:str = "لیست دوره های در حال برگذاری"

    def __init__(self,interact_db:InteractDB):
        self.__interact_db = interact_db

    async def start_command(self,update:Update,context:ContextTypes.DEFAULT_TYPE):

        current_user_info = update.message.from_user
        telegram_user_model = TelegramUserModel(
            user_id=str(current_user_info.id),
            first_name=current_user_info.first_name,
            last_name=current_user_info.last_name,
            username=current_user_info.username,
            language_code=current_user_info.language_code,
        )

        if not self.__interact_db.check_exists(telegram_user_model.check_repeted_item,user_id = str(current_user_info.id)):
            self.__interact_db.insert(telegram_user_model)

        
        reply_text:str = self.__interact_db.fetch_last(WelcomeTextModel()).welcome_text
        if not reply_text:
            reply_text = "Welcome To Our Bot How Can I help you ?"

        keyboards = [
            [KeyboardButton(self.cources_list)],
            [KeyboardButton(self.about_us_text),KeyboardButton(self.contact_us_text)],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboards,resize_keyboard=True)

        await update.message.reply_text(reply_text,reply_markup=reply_markup)


class MyMessageHandler:

    def __init__(self,interact_db:InteractDB):
        self.__interact_db = interact_db

    async def message_handler(self,update:Update,context:ContextTypes.DEFAULT_TYPE):

        text:str = update.message.text

        if text == MyCommandHandler.about_us_text:
            reply_text = self.__interact_db.fetch_last(AboutModel()).about or "درباره ما"
            await update.message.reply_text(reply_text)

        elif text == MyCommandHandler.contact_us_text:
            reply_text = self.__interact_db.fetch_last(ContactModel()).contact or "تماس با ما"
            await update.message.reply_text(reply_text)

        
        elif text == MyCommandHandler.cources_list:

            reply_text:str = ""

            cources_list:list[CourcesModel] = self.__interact_db.fetch_all(CourcesModel())

            for cource in cources_list:
                
                reply_text += f""" 
                <pre>
                <b>{cource.title}</b>
                مدرس : {cource.teacher}
                مدت زمان : {cource.time}
                تاریخ شروع : {cource.start_time or ''}
                </pre>
                """
            print(reply_text)
            await update.message.reply_text(reply_text,parse_mode="HTML")

class BotManager:

    def __init__(self,token:str,proxy:Optional[str] = None):

        db_config = DatabaseConfig("data.db")
        db_interaction = InteractDB(db_config.connect())

        command_handler = MyCommandHandler(db_interaction)
        message_handler = MyMessageHandler(db_interaction)
        
        if proxy is not None:
            try:
                client = httpx.AsyncClient(proxies=proxy)
                self.app = ApplicationBuilder().token(token).client(client).build()
            except:
                raise NetworkError            
        else:
            self.app = ApplicationBuilder().token(token).build()
        
        self.app.add_handler(CommandHandler("start",command_handler.start_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,message_handler.message_handler))

    @classmethod
    def test_connection(self,token:str) -> bool:
        
        bot = Bot(token)
        try:
            asyncio.run(bot.get_me())
            return True
        except:
            return False

    
class BotActions:

    def __init__(self,token:str,proxy:Optional[str] = None) -> None:

        self.__token:str = token
        self.__proxy = proxy

        self.__bot = Bot(self.__token)
        
    @property
    def token(self) -> str:
        return self.__token
    
    @property
    def bot(self) -> Bot:
        return self.__bot

    def test_connection(self) -> bool:

        try:
            asyncio.run(self.bot.get_me())
            return True
        except:
            return False

    async def send_multi_message(self,recivers:list[str],message:str,**kwargs) -> Union[bool,Exception]:

        try:
            for chat_id in recivers:

                await self.send_message(chat_id,message)
            return True
        
        except Exception as e:
            return False,e


    async def send_message(self,reciver:str,message:str,**kwargs) -> bool:

        try:
            await self.bot.send_message(reciver,message,**kwargs)
            return True
        except:
            return False
        
    
    async def send_photo(self,reciver:str,file:bytes,caption:Optional[str] = None) -> Union[bool,Exception]:

        try:
            
            await self.bot.send_photo(reciver,file,caption)
            return True

        except Exception as e:
            return False,e
        
    async def send_multi_image(self,recivers:list[str],file:bytes,caption:Optional[str] = None) -> Union[bool,Exception]:

        try:
            for chat_id in recivers:
                await self.send_photo(chat_id,file,caption)

            return True
        except Exception as e:
            return False,e

    