from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QFont, QIcon
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QMainWindow, QToolButton, QLabel, \
    QMenuBar

from pyqt_frameless_window.framelessWindow import FramelessWindow

from pyqt_top_titlebar_widget import TopTitleBarWidget

from python_color_getter.pythonColorGetter import PythonColorGetter
from pyqt_windows_min_max_close_buttons_widget import WindowsMinMaxCloseButtonsWidget
from pyqt_mac_min_max_close_buttons_widget import MacMinMaxCloseButtonsWidget


class CustomTitlebarWindow(FramelessWindow):
    def __init__(self, main_window: QMainWindow):
        super().__init__(main_window)
        self.__initVal(main_window)
        self.__initUi()

    def __initVal(self, main_window):
        self.__mainWindow = main_window
        self.__menuBar = self.__mainWindow.menuBar()

        self.__windowTitleIconLabel = QLabel()
        self.__titleLbl = QLabel()

        self.__topTitleBar = QWidget()
        self.__btnWidget = QWidget()
        self.__btnHint = Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint

        self.__minimizeBtn = QToolButton()
        self.__maximizeBtn = QToolButton()
        self.__closeBtn = QToolButton()

        self.__styleBasedOnOS = 'Windows'

    def __initUi(self):
        self.__mainWindow.installEventFilter(self)
        self.__menuBar.installEventFilter(self)

        self._dragMenuBarOnlyWayToMoveWindowFlag = True

        lay = QGridLayout()
        lay.addWidget(self.__mainWindow)
        lay.setContentsMargins(self._margin, self._margin, self._margin, self._margin)
        self.setLayout(lay)

        color = self.__menuBar.palette().color(QPalette.Base)
        self.setStyleSheet(f'QWidget {{ background-color: {color.name()} }}')

    def eventFilter(self, obj, e) -> bool:
        if isinstance(obj, QMainWindow):
            # catch the enter event
            if e.type() == 10:
                self.unsetCursor()
                self._resized = False
            # catch the title changed event
            elif e.type() == 33:
                self.__titleLbl.setText(obj.windowTitle())
        elif isinstance(obj, QMenuBar):
            # catch the double click or move event
            if e.type() == 4 or e.type() == 5:
                self.__execMenuBarMoveOrDoubleClickEvent(e)
        elif isinstance(obj, QWidget):
            if obj.objectName() == 'topTitleBar':
                self.unsetCursor()
                if e.type() == 4 or e.type() == 5:
                    self.__execTitleBarMoveOrDoubleClickEvent(e)
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
                if e.type() == 4 and e.button() == Qt.LeftButton:
                    self.__showNormalOrMaximized()
                # move
                else:
                    self._move()

    def __execTitleBarMoveOrDoubleClickEvent(self, e):
        if e.type() == 4 and e.button() == Qt.LeftButton:
            self.__showNormalOrMaximized()
        else:
            self._move()

    def __showNormalOrMaximized(self):
        if self.__styleBasedOnOS == 'Windows':
            self.__showWindowsOSNormalOrMaximized()
        elif self.__styleBasedOnOS == 'Mac':
            self.__showMacOSNormalOrMaximized()

    def __showWindowsOSNormalOrMaximized(self):
        if self.isMaximized():
            self.__maximizeBtn.setText('🗖')
            self.showNormal()
        else:
            self.__maximizeBtn.setText('🗗')
            self.showMaximized()

    def __showMacOSNormalOrMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def setMenuStyle(self, style: str = 'Windows'):
        self.__styleBasedOnOS = style

    def setMinMaxCloseButton(self, hint=Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint, style='Windows'):
        title = self.__mainWindow.windowTitle()
        self.__titleLbl.setText(title)

        lay = QHBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)

        self.__btnHint = hint
        self.__styleBasedOnOS = style

        if self.__styleBasedOnOS == 'Windows':
            self.__btnWidget = WindowsMinMaxCloseButtonsWidget(self.__menuBar, hint)
        elif self.__styleBasedOnOS == 'Mac':
            self.__btnWidget = MacMinMaxCloseButtonsWidget(hint)
        self.initButtonsEvent()
        lay.addWidget(self.__btnWidget)

        # connect the close event with inner widget
        self.closeEvent = self.__mainWindow.closeEvent

        cornerWidget = QWidget()
        cornerWidget.setLayout(lay)

        # set the corner widget that already exists in QMenuBar
        existingCornerWidget = self.__menuBar.cornerWidget(Qt.TopRightCorner)
        if existingCornerWidget:
            lay.insertWidget(0, existingCornerWidget)

        # Place the title on appropriate location of QMenuBar
        if len(self.__menuBar.actions()) > 0:
            lay.insertWidget(0, self.__titleLbl, alignment=Qt.AlignLeft)
        else:
            self.__titleLbl.setContentsMargins(5, 0, 0, 0)
            self.__menuBar.setCornerWidget(self.__titleLbl, Qt.TopLeftCorner)

        self.__menuBar.setCornerWidget(cornerWidget, Qt.TopRightCorner)

    def setSeparatedTitleBar(self, title: str = '', icon_filename: str = '', font: QFont = QFont('Arial', 12), align=Qt.AlignCenter):
        if title:
            self.__mainWindow.setWindowTitle(title)
        else:
            title = self.__mainWindow.windowTitle()

        if icon_filename:
            self.setWindowIcon(QIcon(icon_filename))
        else:
            icon_filename = self.__mainWindow.windowIcon().name()

        self.__topTitleBar = TopTitleBarWidget(self.__menuBar, text=title, font=font, icon_filename=icon_filename, align=align, hint=self.__btnHint)
        self.__topTitleBar.installEventFilter(self)
        self.__topTitleBar.setMouseTracking(True)
        self.__menuBar.removeEventFilter(self)

        iconTitleWidget = self.__topTitleBar.getIconTitleWidget()

        # Remove button widget and title label on QMenuBar
        cornerWidget = self.__menuBar.cornerWidget()
        lay = cornerWidget.layout()
        lay.removeWidget(self.__btnWidget)
        lay.removeWidget(self.__titleLbl)

        self.__btnWidget = self.__topTitleBar.getBtnWidget()
        self.initTitleEvent(iconTitleWidget)
        self.initButtonsEvent()

        lay = self.layout()
        centralWidget = lay.itemAt(0).widget()
        lay.addWidget(self.__topTitleBar, 0, 0, 1, 1)
        lay.addWidget(centralWidget, 1, 0, 1, 1)

    def setDragMenuBarOnlyWayToMoveWindow(self, f: bool):
        self._dragMenuBarOnlyWayToMoveWindowFlag = f

    def getCornerWidget(self):
        return self.__menuBar.cornerWidget()

    def initTitleEvent(self, titleWidget):
        self.__windowTitleIconLabel = titleWidget.getSvgLabel()
        self.__titleLbl = titleWidget.getTextLabel()

    def initButtonsEvent(self):
        self.__minimizeBtn = self.__btnWidget.getMinimizedBtn()
        self.__maximizeBtn = self.__btnWidget.getMaximizedBtn()
        self.__closeBtn = self.__btnWidget.getCloseBtn()

        self.__minimizeBtn.clicked.connect(self.showMinimized)
        self.__maximizeBtn.clicked.connect(self.__showNormalOrMaximized)
        self.__closeBtn.clicked.connect(self.close)