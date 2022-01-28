from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QMainWindow, QToolButton, qApp, QLabel, \
    QMenuBar

from pyqt_frameless_window.framelessWindow import FramelessWindow


class CustomTitlebarWindow(FramelessWindow):
    def __init__(self, main_window: QMainWindow):
        super().__init__(main_window)
        self.__initUi(main_window)

    def __initUi(self, main_window):
        self.__mainWindow = main_window
        self.__mainWindow.enterEvent = self.enterTheMainWindowEvent
        self.__mainWindow.installEventFilter(self)

        self.__menuBar = self.__mainWindow.menuBar()
        self.__menuBar.installEventFilter(self)

        lay = QGridLayout()
        lay.addWidget(self.__mainWindow)
        lay.setContentsMargins(self._margin, self._margin, self._margin, self._margin)
        self.setLayout(lay)

        color = self.__menuBar.palette().color(QPalette.Base)
        self.setStyleSheet(f'QWidget {{ background-color: {color.name()} }}')

    def enterTheMainWindowEvent(self, e):
        print(e, 'unsetCursor')
        self.unsetCursor()
        self._resized = False

    def eventFilter(self, obj, e) -> bool:
        if isinstance(obj, QMainWindow):
            # catch the title changed event
            if e.type() == 33:
                self.__titleLbl.setText(obj.windowTitle())
        elif isinstance(obj, QMenuBar):
            # catch the double click or move event
            if e.type() == 4 or e.type() == 5:
                self.__execMenuBarMoveOrDoubleClickEvent(e)
        return super().eventFilter(obj, e)

    def __execMenuBarMoveOrDoubleClickEvent(self, e):
        p = e.pos()
        if self.__menuBar.actionAt(p):
            pass
        else:
            if self.__menuBar.activeAction():
                pass
            else:
                # double click (show maximized/normal)
                if e.type() == 4:
                    if e.button() == Qt.LeftButton:
                        self.__showNormalOrMaximized()
                # move
                else:
                    self._move()

    def __showNormalOrMaximized(self):
        if self.isMaximized():
            self.__maximizeBtn.setText('🗖')
            self.showNormal()
        else:
            self.__maximizeBtn.setText('🗗')
            self.showMaximized()

    def setMinMaxCloseButton(self, title: str = ''):
        self.__titleLbl = QLabel()
        if title:
            pass
        else:
            title = self.__mainWindow.windowTitle()
        self.__titleLbl.setText(title)

        minimizeBtn = QToolButton()
        minimizeBtn.setText('🗕')
        minimizeBtn.clicked.connect(self.showMinimized)

        self.__maximizeBtn = QToolButton()
        self.__maximizeBtn.setText('🗖')
        self.__maximizeBtn.clicked.connect(self.__showNormalOrMaximized)

        closeBtn = QToolButton()
        closeBtn.setText('🗙')
        closeBtn.clicked.connect(self.close)

        # connect the close event with inner widget
        self.closeEvent = self.__mainWindow.closeEvent

        btns = [minimizeBtn, self.__maximizeBtn, closeBtn]

        menubar_base_color = self.__menuBar.palette().color(QPalette.Base)
        menubar_base_color = menubar_base_color.lighter(150)
        tool_button_style = f'QToolButton ' \
                            f'{{ background: transparent; border: 0; }} ' \
                            f'QToolButton:hover ' \
                            f'{{ background-color: {menubar_base_color.name()}; }}'

        close_button_style = '''QToolButton { background: transparent; border: 0; }
        QToolButton:hover { background-color: #EE0000; }'''

        font_size = qApp.font().pointSize() * 1.2

        lay = QHBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        for btn in btns:
            font = btn.font()
            font.setPointSize(font_size)
            btn.setFont(font)
            btn.setStyleSheet(tool_button_style)
            lay.addWidget(btn)

        closeBtn.setStyleSheet(close_button_style)

        cornerWidget = QWidget()
        cornerWidget.setLayout(lay)

        existingCornerWidget = self.__menuBar.cornerWidget(Qt.TopRightCorner)
        if existingCornerWidget:
            lay.insertWidget(0, existingCornerWidget)
        lay.insertWidget(0, self.__titleLbl, alignment=Qt.AlignLeft)

        self.__menuBar.setCornerWidget(cornerWidget, Qt.TopRightCorner)