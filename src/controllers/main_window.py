from typing import Optional
import asyncio


from PyQt5.QtWidgets import (
    QMainWindow,QMenu,QAction,QTableWidget,QTableWidgetItem,QHeaderView,QAbstractItemView,QLineEdit,QTextEdit,QPushButton,
    QSystemTrayIcon,QWidget
    )
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtGui import QIcon

from .setting_window import SettingWindow
from .readtexts_window import ReadyTextsWindow
from .about_window import AboutUsWindow
from .cources_list_window import CourcesListWindow
from .shcheduling_msg_window import SchedulingMessageWindow

from models.db_config import InteractDB
from models.models import TokenModel,ProxyModel,TelegramUserModel,BotMessagesTiming

from ..tools.worker import BotWorker,MessageQueueSendTimeWorker
from ..tools.widget_helpers import MessageBox,DateTimeConverter

from ..telegram.handler import BotManager




class MainWindow(QMainWindow):

    ui_filename:str = "ui/main_window.ui"
    icon_filename:str = "assets/icon.png"

    def __init__(self,interact_db:Optional[InteractDB] = None) -> None:

        super(MainWindow,self).__init__()
        loadUi(self.ui_filename,self)

        self.setWindowTitle("مدیریت ربات تلگرام")
        self.setWindowIcon(QIcon(self.icon_filename))

        self.interact_db = interact_db
        self.__external_windows_configs()
        self.__menu_bar_config()
        self.start_telegram_bot()
        self.__find_widgets()
        self.__load_data()
        self.start_message_queue_checking()

        self.__system_tray_config()

    def __menu_bar_config(self) -> None:

        self.__menu_bar = self.menuBar()
        # Setting Menu Configs
        setting_action = QAction("تنظیمات اتصال",self)
        setting_action.triggered.connect(self.__menu_connection_setting_clicked)


        ready_texts = QAction("متن های آماده",self)
        ready_texts.triggered.connect(self.__menu_ready_text_clicked)

        about_action = QAction("درباره برنامه",self)
        about_action.triggered.connect(self.__menu_about_clicked)

        reload_connection = QAction("اتصال مجدد",self)
        reload_connection.triggered.connect(self.__menu_reload_connection_clicked)

        setting_menu = QMenu("تنظیمات",self)
        setting_menu.addAction(setting_action)
        setting_menu.addAction(ready_texts)
        setting_menu.addAction(about_action)
        setting_menu.addAction(reload_connection)


        # Cources Menu Configs

        cources_menu = QMenu("دوره ها",self)

        cources_list_action = QAction("لیست دورها",self)
        cources_list_action.triggered.connect(self.__menu_cources_list_clicked)


        cources_menu.addAction(cources_list_action)
        # Refreshing Menu
        refresh_menu = QMenu("به روز رسانی",self)
        refresh_menu.triggered.connect(self.__load_data)


        # Scheduling Menu
        scheduling_menu = QMenu("برنامه ریزی",self)
        
        scheduling_ads_action = QAction("پیام تبلیغاتی",self)
        scheduling_ads_action.triggered.connect(self.__shcheduling_ads_message_menu_clicked)

        scheduling_menu.addAction(scheduling_ads_action)

        # Main Menu Adding
        self.__menu_bar.addMenu(setting_menu)
        self.__menu_bar.addMenu(cources_menu)
        self.__menu_bar.addMenu(refresh_menu)
        self.__menu_bar.addMenu(scheduling_menu)

    

    # External Window Definations
    def __external_windows_configs(self) -> None:

        self.__external_windows = {
            "setting_window" : None,
            "readytexts_window" : None,
            "about_window" : None,
            "cources_window" : None,
            "scheduling_window" : None,
        }

    def __find_widgets(self) -> None:

        self.lst_messages_queue:QTableWidget = self.findChild(QTableWidget,"tblMessageQueue")
        self.lst_messages_queue.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lst_messages_queue.itemDoubleClicked.connect(self.__lst_message_queue_double_clicked)

        self.__tbl_user_info:QTableWidget = self.findChild(QTableWidget,"tblUserInfo")

        self.__txt_message_title:QLineEdit = self.findChild(QLineEdit,"txtMessageTitle")
        self.__txt_user_id:QLineEdit = self.findChild(QLineEdit,"txtUserId")
        self.__txt_message:QTextEdit = self.findChild(QTextEdit,"txtMessage")

        self.__btn_send_message:QPushButton = self.findChild(QPushButton,"btnSendMessage")
        self.__btn_send_message.clicked.connect(self.__btn_send_message_clicked)


    # Menu Bar Events
    def __menu_connection_setting_clicked(self) -> None:
        
        self.__external_windows["setting_window"] = SettingWindow(self,self.interact_db)
        self.__external_windows["setting_window"].show()

    def __menu_ready_text_clicked(self) -> None:
        
        self.__external_windows["readytexts_window"] = ReadyTextsWindow(self,self.interact_db)
        self.__external_windows["readytexts_window"].show()

    def __menu_about_clicked(self) -> None:
        
        self.__external_windows["about_window"] = AboutUsWindow()
        self.__external_windows["about_window"].show()

    def __menu_reload_connection_clicked(self) -> None:
        current_state = self.statusTip()
        if current_state == "اتصال برقرار نیست":
            self.start_telegram_bot()
        else:
            MessageBox.warning_message("اتصال در حال حاضر برقرار است")

    def __menu_cources_list_clicked(self) -> None:
        
        self.__external_windows["cources_window"] = CourcesListWindow(self.interact_db,self)
        self.__external_windows["cources_window"].show()

    def start_telegram_bot(self):

        token = self.__check_token_exists()
        if token:
            
            proxy = self.__check_proxy_exists()
            if proxy:
                self.bot_worker = BotWorker(token = token,proxy=proxy)
            else:
                self.bot_worker = BotWorker(token=token)

            self.bot_worker.connection_success.connect(self.__bot_connection_success)
            self.bot_worker.error_occured.connect(self.__bot_connection_failed)
            self.bot_worker.start()
        else:
            MessageBox.warning_message("توکن تلگرام خالی است")

    def start_message_queue_checking(self):

        token = self.__check_token_exists()
        if token:
            proxy = self.__check_proxy_exists()
            messages_queue:list[BotMessagesTiming] = self.interact_db.filter_fetch(BotMessagesTiming(),done = 0)
            MessageQueueSendTimeWorker.messages_list = messages_queue
            if proxy:
                self.message_queue_worker = MessageQueueSendTimeWorker(token = token,proxy=proxy)
            else:
                self.message_queue_worker = MessageQueueSendTimeWorker(token=token)

            self.message_queue_worker.message_sent.connect(self.__message_queue_sent_event)
            self.message_queue_worker.error_recived.connect(self.__message_queue_error_event)
            self.message_queue_worker.start()


    def __check_token_exists(self) -> bool | str:

        token:str = self.interact_db.fetch_last(TokenModel()).token

        if token:
            return token        
        return False
    
    def __check_proxy_exists(self) -> bool | str:

        proxy = self.interact_db.fetch_last(ProxyModel())

        if proxy:
            return proxy.proxy
        return False
    
    def __bot_connection_failed(self,exception_type:Exception,message:str) -> None:
        MessageBox.warning_message(message)
        self.setStatusTip("اتصال برقرار نیست")

    def __bot_connection_success(self,message:str) -> None:
        self.setStatusTip("اتصال برقرار است")

    def closeEvent(self, a0):
        a0.ignore()
        self.hide()


    def __load_data(self) -> None:
        self.__load_telegram_user_messages()
        self.__load_message_queue()

    def __load_telegram_user_messages(self) -> None:
        
        telegram_users_data:list[TelegramUserModel] = self.interact_db.fetch_all(TelegramUserModel())

        self.__tbl_user_info.setColumnCount(5)
        self.__tbl_user_info.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__tbl_user_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__tbl_user_info.setHorizontalHeaderItem(0,QTableWidgetItem("نام"))
        self.__tbl_user_info.setHorizontalHeaderItem(1,QTableWidgetItem("نام خانوادگی"))
        self.__tbl_user_info.setHorizontalHeaderItem(2,QTableWidgetItem("نام کاربری"))
        self.__tbl_user_info.setHorizontalHeaderItem(3,QTableWidgetItem("کد زبان"))
        self.__tbl_user_info.setHorizontalHeaderItem(4,QTableWidgetItem("Id"))
        self.__tbl_user_info.setRowCount(len(telegram_users_data))

        for index,item in enumerate(telegram_users_data):

            self.__tbl_user_info.setItem(index,0,QTableWidgetItem(item.first_name or ""))
            self.__tbl_user_info.setItem(index,1,QTableWidgetItem(item.last_name or ""))
            self.__tbl_user_info.setItem(index,2,QTableWidgetItem(item.username or ""))
            self.__tbl_user_info.setItem(index,3,QTableWidgetItem(item.language_code or ""))
            self.__tbl_user_info.setItem(index,4,QTableWidgetItem(item.user_id or ""))

    def __load_message_queue(self) -> None:

        messages_queue:list[BotMessagesTiming] = self.interact_db.fetch_all(BotMessagesTiming())

        self.lst_messages_queue.setColumnCount(6)
        self.lst_messages_queue.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lst_messages_queue.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.lst_messages_queue.setHorizontalHeaderItem(0,QTableWidgetItem("id"))
        self.lst_messages_queue.setColumnHidden(0,True)

        self.lst_messages_queue.setHorizontalHeaderItem(1,QTableWidgetItem("تاریخ ارسال"))
        self.lst_messages_queue.setHorizontalHeaderItem(2,QTableWidgetItem("زمان ارسال"))
        self.lst_messages_queue.setHorizontalHeaderItem(3,QTableWidgetItem("انجام شده؟"))
        self.lst_messages_queue.setHorizontalHeaderItem(4,QTableWidgetItem("دریافت کنندگان"))
        self.lst_messages_queue.setHorizontalHeaderItem(5,QTableWidgetItem("متن پیام"))

        self.lst_messages_queue.setRowCount(len(messages_queue))

        for index,item in enumerate(messages_queue):
            
            self.lst_messages_queue.setItem(index,0,QTableWidgetItem(str(item.id)))
            self.lst_messages_queue.setItem(index,1,QTableWidgetItem(item.date))
            self.lst_messages_queue.setItem(index,2,QTableWidgetItem(item.time))
            self.lst_messages_queue.setItem(index,3,QTableWidgetItem("خیر" if not item.done else "بله"))
            self.lst_messages_queue.setItem(index,4,QTableWidgetItem(str(item.recivers)))
            self.lst_messages_queue.setItem(index,5,QTableWidgetItem(item.message))

    def __shcheduling_ads_message_menu_clicked(self) -> None:
        
        self.__external_windows["scheduling_window"] = SchedulingMessageWindow(self,self.interact_db)
        self.__external_windows["scheduling_window"].show()
        

    def __btn_send_message_clicked(self) -> None:

        message_title:str = self.__txt_message_title.text()
        message_text:str = self.__txt_message.toPlainText()
        user_id:str = self.__txt_user_id.text()

        if message_text and user_id:
            token:str = self.interact_db.fetch_last(TokenModel()).token
            if token:
                msg = f"""
                    {message_title}
                    {message_text}
                """
                if BotManager.send_custom_message(token,user_id,msg):
                    MessageBox.success_message("پیام با موفقیت ارسال شد")
                else:
                    MessageBox.warning_message("خطا در ارسال پیام به کاربر مورد نظر")
            else:
                MessageBox.warning_message("توکن تلگرام خالی است")
        else:
            MessageBox.warning_message("لطفا متن پیام و شناسه کاربر را وارد کنید")
    
    def __system_tray_config(self) -> None:

        self.system_tray = QSystemTrayIcon(self)
        self.system_tray.setIcon(QIcon(self.icon_filename))

        fake_widget = QWidget()
        fake_widget.setVisible(False)

        tray_menu = QMenu(fake_widget)
        show_action = QAction("نمایش برنامه")
        quit_action = QAction("خروج")

        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.system_tray.setContextMenu(tray_menu)

        self.system_tray.show()

    def __lst_message_queue_double_clicked(self,item:QTableWidgetItem) -> None:

        clicked_item_id:int = self.lst_messages_queue.item(item.row(),0).text()
        
        if MessageBox.question(self,"آیا از حذف این مورد اطمینان دارید ؟") == MessageBox.yes:

            self.interact_db.remove(BotMessagesTiming(),id=clicked_item_id)
            MessageBox.success_message("با موفقیت حذف شد")
            self.__load_message_queue()


    def __message_queue_sent_event(self,message:str,id:int) -> None:
        
        self.interact_db.remove(BotMessagesTiming(),id)
        self.system_tray.showMessage(message,"ارسال پیام",QIcon(self.icon_filename))
    def __message_queue_error_event(self,message:str) -> None:
        self.system_tray.showMessage(message,"خطا در ارسال پیام",QIcon(self.icon_filename))