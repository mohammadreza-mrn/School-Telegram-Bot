
from typing import Optional


from PyQt5.QtWidgets import (QMenu,QAction,QTableWidgetItem,QWidget,QHeaderView,QAbstractItemView,QTableWidget,QLabel
                             ,QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from models.db_config import InteractDB
from models.models import CourcesModel

from .add_or_edit_cources_window import AddOrEditCourcesWindow
from ..tools.widget_helpers import btn_regular_stylesheet,MessageBox

class CourcesListWindow(QWidget):

    ui_filename:str = "ui/cources_list_window.ui"

    icon_files = {
        "add" : "assets/images/Add.png",
        "delete" : "assets/images/Delete.png",
        "edit" : "assets/images/Edit.png",
        "refresh" : "assets/images/Refresh.png",
    }

    def __init__(self,interact_db:InteractDB,parent:Optional[QWidget] = None) -> None:
        super(CourcesListWindow,self).__init__()
        self.__parent = parent
        self.__interact_db = interact_db
        self.__cource_id:int = 0
        loadUi(self.ui_filename,self)
        self.setWindowTitle("مدیریت دوره ها")
        self.__find_widgets()


    def __find_widgets(self) -> None:

        self.__lst_cources_list:QTableWidget = self.findChild(QTableWidget,"lstCources_list")
        self.__lst_cources_list_load_configs()
        self.__lst_cources_list.itemClicked.connect(self.__lst_cources_list_item_clicked)

        self.__btn_add:QPushButton = self.findChild(QPushButton,"btnAdd")
        btn_regular_stylesheet(self.__btn_add,self.icon_files["add"])
        self.__btn_add.clicked.connect(self.__btn_add_clicked)

        self.__btn_edit:QPushButton = self.findChild(QPushButton,"btnEdit")
        btn_regular_stylesheet(self.__btn_edit,self.icon_files["edit"])
        self.__btn_edit.clicked.connect(self.__btn_edit_clicked)

        self.__btn_delete:QPushButton = self.findChild(QPushButton,"btnDelete")
        btn_regular_stylesheet(self.__btn_delete,self.icon_files["delete"])
        self.__btn_delete.clicked.connect(self.__btn_delete_clicked)

        self.__btn_refresh:QPushButton = self.findChild(QPushButton,"btnRefresh")
        btn_regular_stylesheet(self.__btn_refresh,self.icon_files["refresh"])
        self.__btn_refresh.clicked.connect(self.__btn_refresh_clicked)


    def __lst_cources_list_load_configs(self) -> None:
        
        def base_configs():

            self.__lst_cources_list.setColumnCount(5)
            self.__lst_cources_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.__lst_cources_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.__lst_cources_list.setHorizontalHeaderItem(0,QTableWidgetItem("id"))
            self.__lst_cources_list.setColumnHidden(0, True)
            self.__lst_cources_list.setHorizontalHeaderItem(1,QTableWidgetItem("عنوان دوره"))
            self.__lst_cources_list.setHorizontalHeaderItem(2,QTableWidgetItem("مدت زمان دوره"))
            self.__lst_cources_list.setHorizontalHeaderItem(3,QTableWidgetItem("مدرس"))
            self.__lst_cources_list.setHorizontalHeaderItem(4,QTableWidgetItem("تاریخ شروع"))
            self.__lst_cources_list.setHorizontalHeaderItem(5,QTableWidgetItem("توضیحات"))
        base_configs()

        data = self.__interact_db.fetch_all(CourcesModel())
        columns = ("id","title","time","teacher","start_time","description")

        self.__lst_cources_list.setRowCount(len(data))
        for row in range(len(data)):
            for index,column in enumerate(columns):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                value = getattr(data[row],column)
                item.setText(str(value))
                self.__lst_cources_list.setItem(row,index,item)

    def __btn_add_clicked(self) -> None:
        """Add button clicked event handler"""
        self.__add_cources_window = AddOrEditCourcesWindow(self.__interact_db,self)
        self.__add_cources_window.show()

    def __btn_edit_clicked(self) -> None:
        """ Edit Button clicked event handler """

        if self.__cource_id != 0:
            self.__edit_cources_window = AddOrEditCourcesWindow(self.__interact_db,self)
            self.__edit_cources_window.cource_id = self.__cource_id
            self.__edit_cources_window.show()
        else:
            MessageBox.warning_message("لطفا یک ردیف از اطلاعات پایین را وارد کنید")

    def __btn_delete_clicked(self) -> None:
        """ Delete Button clicked event handler """
        
        if self.__cource_id != 0:
            if MessageBox.question(self,"آیا از حذف این مورد مطمئن هستید ؟") == MessageBox.yes:
                self.__interact_db.remove(CourcesModel(),self.__cource_id)
                self.__lst_cources_list_load_configs()
        else:
            MessageBox.warning_message("لطفا یک ردیف از اطلاعات پایین را وارد کنید")

    def __btn_refresh_clicked(self) -> None:
        """ Refresh Button clicked event handler """
        self.__lst_cources_list_load_configs()


    def __lst_cources_list_item_clicked(self,item:QTableWidgetItem) -> None:

        """ List Cources Item Clicked event handler """
        self.__cource_id = int(self.__lst_cources_list.item(item.row(),0).text())
    