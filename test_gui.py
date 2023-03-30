
import sys

from PyQt6.QtWidgets import QApplication


from mock_gui import CustomWindow
import sales_people_config as spc




if __name__ == "__main__":
    app = QApplication(sys.argv)

    DATABASE = spc.TEST_DB_NAME

    window = CustomWindow(DATABASE)

    # Start the event loop
    app.exec()