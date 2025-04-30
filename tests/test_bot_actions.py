
from unittest import TestCase
import asyncio

from models.db_config import DatabaseConfig,InteractDB
from models.models import TokenModel
from src.telegram.handler import BotActions

class TestBotActions(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseConfig("data.db")
        cls.connection = cls.db.connect()

        cls.interact_db = InteractDB(cls.connection)

        cls.token:str = cls.__get_token()

        if not cls.token:
            raise ValueError("Telegram Token Should have Value")

        return super().setUpClass()
    

    def test_connection(self) -> None:

        bot = BotActions(self.token)
        result = bot.test_connection()
        self.assertTrue(result,"May Cant Connect Telegram")

    def test_send_message(self) -> None:
        
        reciver:str = "6041022419"

        bot = BotActions(self.token)
        result = asyncio.run(bot.send_message(reciver,"Hello This is UnitTest"))
        self.assertTrue(result,f"Cant Send Message To {reciver}")
    
    def test_send_multi_message(self) -> None:

        recivers = ["6041022419"]

        bot = BotActions(self.token)
        result = asyncio.run(bot.send_multi_image(recivers,"Hello This is UnitTest"))
        self.assertTrue(result,f"Cant Send Message To {recivers}")

    def test_send_photo(self) -> None:

        reciver:str = "6041022419"

        bot = BotActions(self.token)
        result = asyncio.run(bot.send_photo(reciver,b"Hello This is UnitTest"))
        self.assertTrue(result)

    def test_send_multi_photo(self) -> None:
        
        recivers = ["6041022419"]

        bot = BotActions(self.token)
        result = asyncio.run(bot.send_multi_image(recivers,b"Hello This is UnitTest"))
        self.assertTrue(result,f"Cant Send Message To {recivers}")


    @classmethod
    def __get_token(cls) -> str:
        
        token:str = cls.interact_db.fetch_last(TokenModel()).token
        return token

    