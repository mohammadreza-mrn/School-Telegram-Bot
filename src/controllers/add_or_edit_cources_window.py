

from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QTextEdit
from PyQt5.uic import loadUi

from models.db_config import InteractDB
from ..tools.widget_helpers import btn_regular_stylesheet
from ..tools.widget_helpers import MessageBox
from models.models import CourcesModel

class AddOrEditCourcesWindow(QWidget):

    ui_filename: str = "ui/add_or_edit_cources_window.ui"

    btn_save_icon_path:str = "assets/images/Save.png"

    def __init__(self, interact_db:InteractDB = None,parent=None) -> None:
        super(AddOrEditCourcesWindow, self).__init__()
        self.__interact_db = interact_db
        self.__parent:QWidget = parent
        self.__cource_id:int = 0
        loadUi(self.ui_filename, self)

        self.__find_widgets()

    @property
    def cource_id(self) -> int:
        return self.__cource_id
    
    @cource_id.setter
    def cource_id(self,cource_id:int) -> None:
        self.__cource_id = cource_id

        self.setWindowTitle("ویرایش دوره")

        cource:CourcesModel = self.__interact_db.fetch_by_id(CourcesModel(id = self.__cource_id))

        self.__txt_cource_title.setText(cource.title)
        self.__txt_cource_time.setText(cource.time)
        self.__txt_cource_start_time.setText(cource.start_time)
        self.__txt_cource_teacher.setText(cource.teacher)
        self.__txt_cource_teacher.setText(cource.teacher)
        self.__txt_cource_description.setText(cource.description)

    def __find_widgets(self) -> None:
        
        self.__txt_cource_title:QLineEdit = self.findChild(QLineEdit,"txtCourceTitle")
        self.__txt_cource_time:QLineEdit = self.findChild(QLineEdit,"txtCourceTime")
        self.__txt_cource_start_time:QLineEdit = self.findChild(QLineEdit,"txtCourceStartTime")
        self.__txt_cource_teacher:QLineEdit = self.findChild(QLineEdit,"txtCourceTeacher")
        self.__txt_cource_description:QTextEdit = self.findChild(QTextEdit,"txtCourceDescription")

        self.__btn_save_cource:QPushButton = self.findChild(QPushButton,"btnSave")
        btn_regular_stylesheet(self.__btn_save_cource,self.btn_save_icon_path)
        self.__btn_save_cource.clicked.connect(self.__save_cource_clicked)


        self.__btn_clear:QPushButton = self.findChild(QPushButton,"btnClear")
        self.__btn_clear.clicked.connect(self.__btn_clear_clicked)

    def __save_cource_clicked(self) -> None:
        
        if self.__validate_inputs():

            cources_model = CourcesModel(
                title = self.__txt_cource_title.text(),
                time = self.__txt_cource_time.text(),
                start_time = self.__txt_cource_start_time.text(),
                teacher = self.__txt_cource_teacher.text(),
                description = self.__txt_cource_description.toPlainText()
            )

            if self.__cource_id == 0:
                self.__interact_db.insert(cources_model)
                MessageBox.success_message("دوره با موفقیت ذخیره شد")
            else:
                if self.__interact_db.update(cources_model,self.__cource_id):
                    MessageBox.success_message("اطلاعات با موفقیت ویرایش شد")
                else:
                    MessageBox.warning_message("خطا در ویرایش اطلاعات")

    def __btn_clear_clicked(self) -> None:
        self.__clear_inputs()

    def __validate_inputs(self) -> bool:

        cource_title:str = self.__txt_cource_title.text()
        cource_time:str = self.__txt_cource_time.text()
        cource_start_time:str = self.__txt_cource_start_time.text()
        cource_teacher:str = self.__txt_cource_teacher.text()
        cource_description:str = self.__txt_cource_description.toPlainText()

        if not cource_title or not cource_time or not cource_teacher or not cource_description:
            MessageBox.warning_message("لطفا همه ی موارد خواسته شده را وارد کنید")
            return False
        
        return True
    
    def __clear_inputs(self) -> bool:

        self.__txt_cource_title.clear()
        self.__txt_cource_time.clear()
        self.__txt_cource_start_time.clear()
        self.__txt_cource_teacher.clear()
        self.__txt_cource_description.clear()