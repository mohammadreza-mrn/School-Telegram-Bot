
from PyQt5.QtWidgets import (QMainWindow,QMenu,QAction,QWidget,QTextBrowser)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon

from models.db_config import InteractDB
from models.models import CourcesModel
from ..tools import resources_rc

class AboutUsWindow(QWidget):
    
    ui_filename:str = "ui/about_window.ui"
    icon_filename:str = "assets/icon.png"

    def __init__(self,interact_db:InteractDB = None,parent:QWidget = None) -> None:
        
        super(AboutUsWindow,self).__init__()
        self.__interact_db = interact_db
        self.__parent = parent
        loadUi(self.ui_filename,self)
        self.setWindowIcon(self.icon_filename)
        self.setWindowTitle("درباره برنامه")

        self.__find_widgets()

    def __find_widgets(self) -> None:
        
        self.__text_browser:QTextBrowser = self.findChild(QTextBrowser,"textBrowser")

    def __load_database(self) -> None:

        self.__interact_db.fetch_all(CourcesModel())


    