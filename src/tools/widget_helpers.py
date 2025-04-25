
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit,QMessageBox,QWidget
import jdatetime
from datetime import datetime

class MessageBox:

    yes = QMessageBox.Yes
    no = QMessageBox.No

    icon_filename:str = "assets/icon.png"

    @classmethod
    def success_message(cls,text:str) -> None:

        msg = QMessageBox()
        msg.setWindowIcon(QIcon(cls.icon_filename))
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("موفقیت")
        msg.exec_()

    @classmethod
    def error_message(cls,text:str) -> None:

        msg = QMessageBox()
        msg.setWindowIcon(QIcon(cls.icon_filename))
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle("خطا")
        msg.exec_()

    @classmethod
    def warning_message(cls,text:str) -> None:

        msg = QMessageBox()
        msg.setWindowIcon(QIcon(cls.icon_filename))
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle("هشدار")
        msg.exec_()

    @classmethod
    def question(cls,parent:QWidget,question_text:str):
        return QMessageBox.question(parent,"سوال",question_text,QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
    


class DateTimeConverter:

    def __init__(self,date_time:datetime | str) -> None:
        
        if isinstance(date_time,datetime):
            self.__datetime = date_time
        elif isinstance(date_time,str):
            self.__datetime = datetime.strptime(date_time, "%Y/%m/%d %H:%M")

    def to_shamsi(self) -> jdatetime.datetime:
        return jdatetime.datetime.fromgregorian(
            year=self.__datetime.year,
            month=self.__datetime.month,
            day=self.__datetime.day,
            hour=self.__datetime.hour,
            minute=self.__datetime.minute,
            second=self.__datetime.second
        )
    def to_gregorian(self) -> datetime:
        return jdatetime.datetime(
            year=self.__datetime.year,
            month=self.__datetime.month,
            day=self.__datetime.day,
            hour=self.__datetime.hour,
            minute=self.__datetime.minute,
            second=self.__datetime.second
        ).togregorian()
    
    def __str__(self):        
        return self.__datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    @classmethod
    def check_time_equals(cls,firsttime:datetime,secondtime:datetime) -> bool:
        
        return (firsttime.year == secondtime.year and firsttime.month == secondtime.month) and \
        (firsttime.day == secondtime.day) and (firsttime.hour == secondtime.hour) \
        and (firsttime.minute == secondtime.minute) and (firsttime.second == secondtime.second)
            
        

def btn_regular_stylesheet(btn:QLineEdit,icon_path:str) -> None:
    """
    Set the stylesheet for a button with an icon.
    :param btn: The button to set the stylesheet for.
    :param icon_path: The path to the icon file.
    """
    style = """
        background-image: url('{0}');
        background-repeat: no-repeat;
        background-position: center;
        border: none;
    """.format(icon_path)
    btn.setStyleSheet(style)


