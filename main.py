import sys
from PyQt5.QtWidgets import QApplication
import qdarkstyle

from src.controllers.main_window import MainWindow
from models.db_config import DatabaseConfig,InteractDB

def main():

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setQuitOnLastWindowClosed(False)

    db_config = DatabaseConfig("data.db")
    connection = db_config.connect()

    interact_db = InteractDB(connection)

    main_window = MainWindow(interact_db)
    main_window.show()

    sys.exit(app.exec_())




if __name__ == "__main__":
    main()