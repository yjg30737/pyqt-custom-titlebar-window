from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqt_custom_titlebar_window.customTitlebarWindow import CustomTitlebarWindow
from sample.fontWidget import FontWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')

        self.__fontWidget = FontWidget()
        self.setCentralWidget(self.__fontWidget)

        # Example menubar
        menu = self.menuBar()
        menu.addAction('File')
        menu.addAction('Edit')
        menu.addAction('View')
        menu.addAction('Help')
        self.setMenuBar(menu)

    def getFontWidget(self):
        return self.__fontWidget

if __name__ == "__main__":
  import sys

  app = QApplication(sys.argv)
  window = MainWindow()
  customTitlebarWindow = CustomTitlebarWindow(window)
  customTitlebarWindow.setTopTitleBar(icon_filename='icon.svg')
  customTitlebarWindow.setButtonHint(hint=['min', 'max', 'close'])
  customTitlebarWindow.setButtons()
  customTitlebarWindow.show()
  app.exec_()