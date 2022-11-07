import sys

from PyQt6.QtWidgets import QApplication

from src.qt.main_window import MainWindow

app = QApplication(sys.argv)

main_window = MainWindow()
main_window.show()
