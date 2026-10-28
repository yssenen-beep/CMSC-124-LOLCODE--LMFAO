import sys
from PyQt6.QtWidgets import QApplication

from gui.gui import ourGUI # import gui

def main():
    app = QApplication(sys.argv)
    window = ourGUI()
    window.show()
    sys.exit(app.exec())

main()