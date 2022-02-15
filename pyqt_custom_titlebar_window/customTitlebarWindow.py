from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QFont, QIcon, QPixmap, QColor
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QMainWindow, QToolButton, qApp, QLabel, \
    QMenuBar

from python_color_getter.pythonColorGetter import PythonColorGetter
from pyqt_frameless_window.framelessWindow import FramelessWindow
from pyqt_mac_min_max_close_buttons_widget import MacMinMaxCloseButtonsWidget


class CustomTitlebarWindow(FramelessWindow):
    def __init__(self, main_window: QMainWindow):
        super().__init__(main_window)
        self.__initVal(main_window)
        self.__initUi()

    def __initVal(self, main_window):
        self.__mainWindow = main_window
        self.__menuBar = self.__mainWindow.menuBar()
        self.__titleLbl = QLabel()
        self.__minMaxCloseBtnStyle = 'Windows'
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
            if self.__minMaxCloseBtnStyle == 'Windows':
                self.__maximizeBtn.setText('🗖')
            self.showNormal()
        else:
            if self.__minMaxCloseBtnStyle == 'Windows':
                self.__maximizeBtn.setText('🗗')
            self.showMaximized()

    def setMinMaxCloseButton(self, hint=Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint, style='Windows'):
        title = self.__mainWindow.windowTitle()
        self.__titleLbl.setText(title)

        lay = QHBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)

        self.__minMaxCloseBtnStyle = style
        if self.__minMaxCloseBtnStyle == 'Windows':
            lay.setSpacing(0)

            self.__minimizeBtn.setText('🗕')
            self.__maximizeBtn.setText('🗖')
            self.__closeBtn.setText('🗙')

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

            for btn in btns:
                font = btn.font()
                font.setPointSize(font_size)
                btn.setFont(font)
                btn.setStyleSheet(tool_button_style)

            self.__closeBtn.setStyleSheet(close_button_style)
        elif self.__minMaxCloseBtnStyle == 'Mac':
            lay.setSpacing(2)
            macMinMaxCloseButtonsWidget = MacMinMaxCloseButtonsWidget()
            self.__minimizeBtn = macMinMaxCloseButtonsWidget.getMinimizedBtn()
            self.__maximizeBtn = macMinMaxCloseButtonsWidget.getMaximizedBtn()
            self.__closeBtn = macMinMaxCloseButtonsWidget.getCloseBtn()

        self.__minimizeBtn.clicked.connect(self.showMinimized)
        self.__maximizeBtn.clicked.connect(self.__showNormalOrMaximized)
        self.__closeBtn.clicked.connect(self.close)

        # connect the close event with inner widget
        self.closeEvent = self.__mainWindow.closeEvent

        if hint:
            if hint == Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint:
                lay.addWidget(self.__minimizeBtn)
                lay.addWidget(self.__maximizeBtn)
                lay.addWidget(self.__closeBtn)
            elif hint == Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint:
                lay.addWidget(self.__minimizeBtn)
                lay.addWidget(self.__closeBtn)
            elif hint == Qt.WindowCloseButtonHint:
                lay.addWidget(self.__closeBtn)
            else:
                #todo for another type of flags
                pass

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

    def setSeparatedTitleBar(self, icon: QIcon = QIcon(), font: QFont = QFont('Arial', 12), align=Qt.AlignCenter):
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

        lay = QHBoxLayout()
        lay.addWidget(self.__windowTitleIconLabel)
        lay.addWidget(self.__titleLbl)
        lay.setAlignment(align)
        lay.setContentsMargins(2, 2, 2, 2)

        menubar_base_color = self.__menuBar.palette().color(QPalette.Base)

        self.__topTitleBar.setObjectName('topTitleBar')
        self.__topTitleBar.setStyleSheet(f'QWidget {{ background-color: {menubar_base_color.name()}; }}')
        self.__topTitleBar.setMinimumHeight(self.__titleLbl.fontMetrics().height())
        self.__topTitleBar.setLayout(lay)

        title_lbl_r, title_lbl_g, title_lbl_b = PythonColorGetter.get_complementary_color(menubar_base_color.red(),
                                                                                          menubar_base_color.green(),
                                                                                          menubar_base_color.blue())
        title_lbl_color = QColor(title_lbl_r, title_lbl_g, title_lbl_b)
        self.__titleLbl.setStyleSheet(f'QLabel {{ color: {title_lbl_color.name()}; }}')

        self.__topTitleBar.installEventFilter(self)
        self.__topTitleBar.setMouseTracking(True)
        self.__menuBar.removeEventFilter(self)

        lay = self.layout()
        centralWidget = lay.itemAt(0).widget()
        lay.addWidget(self.__topTitleBar, 0, 0, 1, 1)
        lay.addWidget(centralWidget, 1, 0, 1, 1)

    def setDragMenuBarOnlyWayToMoveWindow(self, f: bool):
        self._dragMenuBarOnlyWayToMoveWindowFlag = f

    def getCornerWidget(self):
        return self.__menuBar.cornerWidget()