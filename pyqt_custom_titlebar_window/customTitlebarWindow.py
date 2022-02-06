from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QMainWindow, QToolButton, qApp, QLabel, \
    QMenuBar

from pyqt_frameless_window.framelessWindow import FramelessWindow


class CustomTitlebarWindow(FramelessWindow):
    def __init__(self, main_window: QMainWindow):
        super().__init__(main_window)
        self.__initVal(main_window)
        self.__initUi()

    def __initVal(self, main_window):
        self.__mainWindow = main_window
        self.__menuBar = self.__mainWindow.menuBar()
        self.__titleLbl = QLabel()
        self.__minimizeBtn = QToolButton()
        self.__maximizeBtn = QToolButton()
        self.__closeBtn = QToolButton()
        self.__topTitleBar = QWidget()
        self.__windowTitleIconLabel = QLabel()

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
        if self.isMaximized():
            self.__maximizeBtn.setText('🗖')
            self.showNormal()
        else:
            self.__maximizeBtn.setText('🗗')
            self.showMaximized()

    def setMinMaxCloseButton(self):
        title = self.__mainWindow.windowTitle()
        self.__titleLbl.setText(title)

        self.__minimizeBtn.setText('🗕')
        self.__minimizeBtn.clicked.connect(self.showMinimized)

        self.__maximizeBtn.setText('🗖')
        self.__maximizeBtn.clicked.connect(self.__showNormalOrMaximized)

        self.__closeBtn.setText('🗙')
        self.__closeBtn.clicked.connect(self.close)

        # connect the close event with inner widget
        self.closeEvent = self.__mainWindow.closeEvent

        btns = [self.__minimizeBtn, self.__maximizeBtn, self.__closeBtn]

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

        self.__closeBtn.setStyleSheet(close_button_style)

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

    def setSeparatedTitleBar(self, icon: QIcon = QIcon(), font: QFont = QFont('Arial', 12)):
        if icon.isNull():
            self.__windowTitleIconLabel.setVisible(False)
        else:
            self.setWindowIcon(icon)
            icon_size = font.pointSize()
            icon = icon.pixmap(icon_size * 1.5, icon_size * 1.5)
            pixmap = QPixmap(icon)
            self.__windowTitleIconLabel.setPixmap(pixmap)
            self.__windowTitleIconLabel.setMaximumWidth(pixmap.width())

        self.__titleLbl.setFont(font)
        self.__titleLbl.setStyleSheet('QLabel { color: white; }')

        lay = QHBoxLayout()
        lay.addWidget(self.__windowTitleIconLabel)
        lay.addWidget(self.__titleLbl)
        lay.setAlignment(Qt.AlignCenter)
        lay.setContentsMargins(2, 2, 2, 2)

        self.__topTitleBar.setObjectName('topTitleBar')
        self.__topTitleBar.setStyleSheet('QWidget { background-color: #444; }')
        self.__topTitleBar.setMinimumHeight(self.__titleLbl.fontMetrics().height())
        self.__topTitleBar.setLayout(lay)

        self.__topTitleBar.installEventFilter(self)
        self.__topTitleBar.setMouseTracking(True)
        self.__menuBar.removeEventFilter(self)

        lay = self.layout()
        centralWidget = lay.itemAt(0).widget()
        lay.addWidget(self.__topTitleBar, 0, 0, 1, 1)
        lay.addWidget(centralWidget, 1, 0, 1, 1)

    def setDragMenuBarOnlyWayToMoveWindow(self, f: bool):
        self._dragMenuBarOnlyWayToMoveWindowFlag = f