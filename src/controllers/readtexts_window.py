
from typing import Optional

from PyQt5.QtWidgets import (QMainWindow,QMenu,QAction,QWidget,QLineEdit,QPushButton,QListWidget,QTextEdit)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon

from models.db_config import InteractDB
from models.models import AboutModel,ContactModel,WelcomeTextModel
from ..tools.widget_helpers import MessageBox

class ReadyTextsWindow(QWidget):

    ui_filename:str = "ui/readytexts_window.ui"
    icon_filename:str = "assets/icon.png"

    def __init__(self,parent:Optional[QWidget] = None,interact_db:Optional[InteractDB] = None):
        
        super(ReadyTextsWindow,self).__init__()
        loadUi(self.ui_filename,self)
        self.parent = parent
        self.interact_db = interact_db
        self.setWindowTitle("متن های آماده")
        self.setWindowIcon(QIcon(self.icon_filename))
        self.__find_widgets()
        self.__load_database()

    def __find_widgets(self) -> None:
        
        # TxtAbout
        self.__txt_about:QTextEdit = self.findChild(QTextEdit,"txtAbout")
        self.__btn_save_about:QPushButton = self.findChild(QPushButton,"btnSaveAbout")

        # TxtContact
        self.__txt_contact:QTextEdit = self.findChild(QTextEdit,"txtContact")
        self.__btn_save_contact:QPushButton = self.findChild(QPushButton,"btnSaveContact")

        #TxtWelcome
        self.__txt_welcome:QTextEdit = self.findChild(QTextEdit,"txtWelcomeText")
        self.__btn_save_welcome:QPushButton = self.findChild(QPushButton,"btnSaveWelcomeText")

        #btnAbout Click Event
        self.__btn_save_about.clicked.connect(self.__btn_save_about_clicked)

        # btnContact Click Event
        self.__btn_save_contact.clicked.connect(self.__btn_save_contact_clicked)

        # btnsSaveWelcome Click Event
        self.__btn_save_welcome.clicked.connect(self.__btn_save_welcome_clicked)

    def __btn_save_about_clicked(self) -> None:
        
        about_text:str = self.__txt_about.toPlainText()

        if about_text:
            about_model = AboutModel(about_text)
            self.interact_db.insert(about_model)
            MessageBox.success_message("متن شما با موفقیت ثبت شد")
        else:
            MessageBox.warning_message("لطفا متن درباره ما را وارد کنید")

    def __btn_save_contact_clicked(self) -> None:
        
        contact_text:str = self.__txt_contact.toPlainText()

        if contact_text:
            contact_model = ContactModel(contact_text)
            self.interact_db.insert(contact_model)
            MessageBox.success_message("متن شما با موفقیت ثبت شد")
        else:
            MessageBox.warning_message("لطفا متن تماس با ما را وارد کنید")

    def __btn_save_welcome_clicked(self) -> None:

        welcome_text:str = self.__txt_welcome.toPlainText()

        if welcome_text:
            welcomtext_model = WelcomeTextModel(welcome_text=welcome_text)
            self.interact_db.insert(welcomtext_model)
            MessageBox.success_message("متن شما با موفقیت ثبت شد")
        else:
            MessageBox.warning_message("لطفا متن خوش آمد گویی را وارد کنید")

    def __load_database(self) -> None:

        # load AboutUs Text
        about_model = AboutModel()
        about_model:AboutModel = self.interact_db.fetch_last(about_model)
        self.__txt_about.setText(about_model.about)

        # load contact Text
        contact_model = ContactModel()
        contact_model:ContactModel = self.interact_db.fetch_last(contact_model)
        self.__txt_contact.setText(contact_model.contact)

        # load welcome Text
        welcome_model = WelcomeTextModel()
        welcome_model:WelcomeTextModel = self.interact_db.fetch_last(welcome_model)
        self.__txt_welcome.setText(welcome_model.welcome_text)


    