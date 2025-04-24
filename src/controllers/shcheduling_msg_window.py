
from typing import Optional

from PyQt5.QtWidgets import (
    QMenu,QAction,QTableWidget,QTableWidgetItem,QAbstractItemView,QLineEdit,QTextEdit,QPushButton,QCheckBox,QDateTimeEdit,
    QWidget,QListWidget,QFileDialog,QLabel
)
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt,QPoint,QDate

from models.db_config import InteractDB
from models.models import TelegramUserModel,TokenModel,BotMessagesTiming

from ..tools.widget_helpers import MessageBox,DateTimeConverter
from ..telegram.handler import BotManager

from ..tools.worker import MessageQueueSendTimeWorker

class SchedulingMessageWindow(QWidget):

    ui_filename:str = "ui/scheduling_message.ui"
    window_title:str = "زمانبندی پیام"

    def __init__(self,parent:Optional[QWidget] = None,interact_db:Optional[InteractDB] = None,) -> None:
        
        super(SchedulingMessageWindow,self).__init__()
        self.__parent = parent
        self.__interact_db = interact_db
        loadUi(self.ui_filename,self)
        self.setWindowTitle(self.window_title)

        self.__recivers_list:set[str] = set()
        self.__filename:str = ""

        self.__find_widgets()
        self.__load_data()

    def __find_widgets(self) -> None:

        self.__lbl_filename:QLabel = self.findChild(QLabel,"lblFilename")

        self.__txt_message_title:QLineEdit = self.findChild(QLineEdit,"txtMessageTitle")
        self.__txt_message_text:QTextEdit = self.findChild(QTextEdit,"txtMessage")
        
        self.__chk_send_all:QCheckBox = self.findChild(QCheckBox,"chkReciveAll")
        self.__chk_send_all.clicked.connect(self.__chk_send_all_clicked)

        self.__chk_send_now:QCheckBox = self.findChild(QCheckBox,"chkSendNow")
        self.__chk_send_now.clicked.connect(self.__chk_send_now_clicked)

        self.__send_time:QDateTimeEdit = self.findChild(QDateTimeEdit,"txtSendTime")
        self.__send_time.setMinimumDate(QDate(1400,1,1))

        self.__btn_send:QPushButton = self.findChild(QPushButton,"btnSend")
        self.__btn_send.clicked.connect(self.__btn_send_clicked)

        self.__btn_choose_picture = self.findChild(QPushButton,"btnChoosePicture")
        self.__btn_choose_picture.clicked.connect(self.__btn_choose_picture_clicked)

        self.__lst_recivers:QListWidget = self.findChild(QListWidget,"lstReciversUsers")
        self.__lst_recivers.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__lst_recivers.customContextMenuRequested.connect(self.__open_lst_context_menu)


        self.__tbl_all_users:QTableWidget = self.findChild(QTableWidget,"tblWholeUsers")
        self.__tbl_all_users.itemClicked.connect(self.__tbl_all_users_item_clicked)


    def __chk_send_all_clicked(self) -> None:
        
        if self.__tbl_all_users.isEnabled() and self.__lst_recivers.isEnabled():
            self.__tbl_all_users.setEnabled(False)
            self.__lst_recivers.setEnabled(False)
        else:
            self.__tbl_all_users.setEnabled(True)
            self.__lst_recivers.setEnabled(True)

    def __chk_send_now_clicked(self) -> None:
        
        if self.__send_time.isEnabled():
            self.__send_time.setEnabled(False)
        else:
            self.__send_time.setEnabled(True)

    def __btn_send_clicked(self) -> None:
        
        if self.__validate_inputs():

            message_title:str = self.__txt_message_title.text()
            message_text:str = self.__txt_message_text.toPlainText()
            send_time:str = self.__send_time.text()

            send_now_check:bool = self.__chk_send_now.isChecked()

            token:str = self.__interact_db.fetch_last(TokenModel()).token
            if token:
                if send_now_check:
                    
                    message:str = f""" 
                        {message_title} \n {message_text}
                    """

                    try:
                        if not self.__chk_send_all.isChecked():
                            if self.__filename != "":
                                BotManager.send_many_photo(token,self.__recivers_list,self.__filename,message)
                            else:
                                BotManager.send_many_messages(token,self.__recivers_list,message)
                        else:
                            all_users:list[TelegramUserModel] = self.__interact_db.fetch_all(TelegramUserModel())
                            if self.__filename != "":
                                BotManager.send_many_photo(token,self.__recivers_list,self.__filename,message)
                            else:
                                BotManager.send_many_messages(token,[item.user_id for item in all_users],message)
                        MessageBox.success_message("پیام با موفقیت ارسال شد")
                    except:
                        MessageBox.warning_message("خطا در ارسال پیام")
                        
                    

                else:
                    gregorian = DateTimeConverter(send_time).to_gregorian()

                    date:str = gregorian.strftime("%Y/%m/%d")
                    time:str = gregorian.strftime("%H:%M")

                    recivers = ""

                    if self.__chk_send_all.isChecked():
                        all_users:list[TelegramUserModel] = self.__interact_db.fetch_all(TelegramUserModel())
                        recivers = "-".join([item.user_id for item in all_users])
                        for user in all_users:
                            self.__recivers_list.add(user.user_id)
                    else:
                        if len(self.__recivers_list) >= 0:
                            recivers = "-".join(self.__recivers_list)
                        
                    if len(self.__recivers_list) > 0:
                        bot_message_timing = BotMessagesTiming(time = time,date = date,message = message_text,recivers=recivers)
                        self.__interact_db.insert(bot_message_timing)
                        message_list = self.__interact_db.filter_fetch(BotMessagesTiming(),done = 0)
                        MessageQueueSendTimeWorker.messages_list = message_list
                        MessageBox.success_message("به صف ارسال اضافه شد")

                        # Adding New Row To Parent QLiestWidget Window
                        self.__adding_new_row_to_messages_quque(bot_message_timing)
                        self.__recivers_list.clear()

                    else:
                        MessageBox.warning_message("لطفا لیست دریافت کنندگان را وارد کنید")
            else:
                MessageBox.warning_message("توکن تلگرام خالی است")


    def __validate_inputs(self) -> bool:

        message_title:str = self.__txt_message_title.text()
        message_text:str = self.__txt_message_text.toPlainText()
        send_time:str = self.__send_time.text()

        if self.__chk_send_now.isChecked() and not send_time:
            MessageBox.warning_message("لطفا تاریخ ارسال را وارد کنید")
            return False

        if not message_text and not message_title:
            MessageBox.warning_message("لطفا موارد عنوان پیام و متن پیام را وارد کنید")
            return False
        
        return True
    
    def __load_data(self) -> None:
        
        self.__all_users_configs()


    def __all_users_configs(self) -> None:
        
        self.__tbl_all_users.setColumnCount(4)
        self.__tbl_all_users.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__tbl_all_users.setHorizontalHeaderItem(0,QTableWidgetItem("نام"))
        self.__tbl_all_users.setHorizontalHeaderItem(1,QTableWidgetItem("نام خانوادگی"))
        self.__tbl_all_users.setHorizontalHeaderItem(2,QTableWidgetItem("نام کاربری"))
        self.__tbl_all_users.setHorizontalHeaderItem(4,QTableWidgetItem("Id"))


        all_users:list[TelegramUserModel] = self.__interact_db.fetch_all(TelegramUserModel())

        self.__tbl_all_users.setRowCount(len(all_users))

        for index,user in enumerate(all_users):

            self.__tbl_all_users.setItem(index,0,QTableWidgetItem(user.first_name))
            self.__tbl_all_users.setItem(index,1,QTableWidgetItem(user.last_name))
            self.__tbl_all_users.setItem(index,2,QTableWidgetItem(user.username))
            self.__tbl_all_users.setItem(index,3,QTableWidgetItem(user.user_id))

    def __tbl_all_users_item_clicked(self,item:QTableWidgetItem) -> None:
        
        item_text = self.__tbl_all_users.item(item.row(),3).text()
        
        if item_text not in self.__recivers_list:
            self.__recivers_list.add(item_text)
            self.__lst_recivers.addItem(item_text)
        
    def __open_lst_context_menu(self,position:QPoint) -> None:
        
        def clear_recivers():
            self.__lst_recivers.clear()
            self.__recivers_list.clear()

        menu = QMenu()

        clear_action = QAction("تمیز کردن لیست",self)
        clear_action.triggered.connect(clear_recivers)

        menu.addAction(clear_action)

        menu.exec_(self.__lst_recivers.viewport().mapToGlobal(position))


    def __adding_new_row_to_messages_quque(self,current_data:BotMessagesTiming) -> None:

        # adding new row to parent window messages queue table widget
        current_row:int = self.__parent.lst_messages_queue.rowCount()
        self.__parent.lst_messages_queue.setRowCount(current_row + 1)
        self.__parent.lst_messages_queue.setItem(current_row,0,QTableWidgetItem(str(current_data.id)))
        self.__parent.lst_messages_queue.setItem(current_row,1,QTableWidgetItem(current_data.date))
        self.__parent.lst_messages_queue.setItem(current_row,2,QTableWidgetItem(current_data.time))
        self.__parent.lst_messages_queue.setItem(current_row,3,QTableWidgetItem("خیر" if not current_data.done else "بله"))
        self.__parent.lst_messages_queue.setItem(current_row,4,QTableWidgetItem(str(current_data.recivers)))
        self.__parent.lst_messages_queue.setItem(current_row,5,QTableWidgetItem(current_data.message))

    def __btn_choose_picture_clicked(self) -> None:
        
        filename:str = QFileDialog.getOpenFileName(self,"انتخاب فایل")[0]
        self.__filename = filename
        self.__lbl_filename.setText(self.__filename)