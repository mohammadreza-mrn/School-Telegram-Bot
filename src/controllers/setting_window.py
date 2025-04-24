
from PyQt5.QtWidgets import (QMainWindow,QMenu,QAction,QWidget,QLineEdit,QPushButton,QListWidget,QListWidgetItem)
from PyQt5.uic import loadUi

from models.db_config import InteractDB
from models.models import TokenModel,ProxyModel

from ..tools.widget_helpers import MessageBox
from src.telegram.handler import BotManager

class SettingWindow(QWidget):

    ui_filename:str = "ui/setting_window.ui"
    window_title:str = "تنظیمات اتصال به تلگرام"

    def __init__(self, parent = None,interact_db:InteractDB = None):
        
        super(SettingWindow,self).__init__()
        self.parent = parent
        self.interact_db = interact_db
        loadUi(self.ui_filename,self)

        self.setWindowTitle(self.window_title)
        
        
        self.__define_child_widgets()
        self.__load_database()


    def __define_child_widgets(self) -> None:

        self.__txt_token:QLineEdit = self.findChild(QLineEdit,"txtTokenText")
        self.__txt_token.setEnabled(True)
        self.__txt_token.mouseDoubleClickEvent = self.__txt_token_double_clicked


        self.__txt_proxy:QLineEdit = self.findChild(QLineEdit,"txtProxy")


        self.__btn_save_token:QPushButton = self.findChild(QPushButton,"btnSave")
        self.__btn_save_token.clicked.connect(self.__btn_save_token_clicked)



        self.__btn_test_connection:QPushButton = self.findChild(QPushButton,"btnTestConnection")
        self.__btn_test_connection.clicked.connect(self.__btn_test_connection_clicked)
        
        self.__lst_connection_logs:QListWidget = self.findChild(QListWidget,"lstLogs")



    def __txt_token_double_clicked(self,a0) -> None:
        self.__txt_token.setEnabled(True)


    def __btn_save_token_clicked(self) -> None:
        
        token:str = self.__txt_token.text()
        proxy:str = self.__txt_proxy.text()
        if token:
            token_model = TokenModel(token)
            self.interact_db.insert(token_model)
            
            if proxy:
                proxy_model = ProxyModel(proxy=proxy)
                self.interact_db.insert(proxy_model)

            MessageBox.success_message("اطلاعات جدید با موفقیت ثبت شد")
        else:
            MessageBox.error_message("لطفا توکن را وارد کنید")

    def __load_database(self) -> None:

        # load last token
        token:TokenModel = self.interact_db.fetch_last(TokenModel())
        self.__txt_token.setText(token.token)

        # load proxy if exists
        proxy:ProxyModel = self.interact_db.fetch_last(ProxyModel())
        if proxy:
            self.__txt_proxy.setText(proxy.proxy)
        
    def __btn_test_connection_clicked(self) -> None:

        self.__lst_connection_logs.clear()

        self.__btn_test_connection.setEnabled(False)
        self.__lst_connection_logs.addItem("در حال اتصال ...")
        token:str = self.__txt_token.text()
        result = BotManager.test_connection(token)

        self.__lst_connection_logs.addItem("دریافت پاسخ ...")
        if result:
            self.__lst_connection_logs.addItem("اتصال موفق بود")
            MessageBox.success_message("اتصال موفق بود")
        else:
            self.__lst_connection_logs.addItem("اتصال نا موفق بود")
            MessageBox.warning_message("اتصال نا موفق بود")

        self.__btn_test_connection.setEnabled(True)
