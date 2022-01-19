from PyQt5.QtWidgets import QMainWindow, QMenuBar, QMenu, QStatusBar, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__setMenuBar()
        self.__setStatusBar()

    def __setMenuBar(self):
        menuBar = QMenuBar()

        filemenu = QMenu('File', self)
        editmenu = QMenu('Edit', self)

        menuBar.addMenu(filemenu)
        menuBar.addMenu(editmenu)

        self.setMenuBar(menuBar)

    def __setStatusBar(self):
        statusBar = QStatusBar()
        statusBar.setSizeGripEnabled(False)
        statusBar.addWidget(QPushButton('ABC'))
        self.setStatusBar(statusBar)