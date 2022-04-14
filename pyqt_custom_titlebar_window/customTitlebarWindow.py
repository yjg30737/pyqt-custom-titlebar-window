from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QFont, QIcon
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QMainWindow, QPushButton, QLabel, \
    QMenuBar, QToolButton, qApp

from pyqt_frameless_window.framelessWindow import FramelessWindow

from pyqt_top_titlebar_widget import TopTitleBarWidget

from pyqt_windows_min_max_close_buttons_widget import WindowsMinMaxCloseButtonsWidget
from pyqt_mac_min_max_close_buttons_widget import MacMinMaxCloseButtonsWidget
from python_get_absolute_resource_path.getAbsoulteResourcePath import get_absolute_resource_path


class CustomTitlebarWindow(FramelessWindow):
    def __init__(self, widget: QWidget):
        super().__init__(widget)
        self.__initVal(widget)
        self.__initUi()

    def __initVal(self, widget):
        self.setObjectName('titleBar')

        self.__widget = widget
        self.__widget.setObjectName('mainWidget')
        self.__menubar = ''

        # if inner widget type is QMainWindow, set menu bar as navigation widget
        # navigation widget is the widget which is able to drag to move the window, double click to maximize/normal
        if isinstance(self.__widget, QMainWindow):
            self.__menubar = self.__widget.menuBar()
            self.__menubar.setObjectName('navWidget')

        self.__windowTitleIconLabel = QLabel()
        self.__titleLbl = QLabel()

        self.__topTitleBar = QWidget()
        self.__btnWidget = QWidget()
        self.__btnHint = ['min', 'max', 'close']

        self.__minimizeBtn = QPushButton()
        self.__maximizeBtn = QPushButton()
        self.__closeBtn = QPushButton()

        self.__styleBasedOnOS = qApp.platformName()
        if self.__styleBasedOnOS == 'windows' or self.__styleBasedOnOS == 'mac':
            pass
        else:
            self.__styleBasedOnOS = 'windows'

    def __initUi(self):
        self.__widget.installEventFilter(self)
        self.installEventFilter(self)

        # connect the close event with inner widget
        self.closeEvent = self.__widget.closeEvent

        lay = QGridLayout()
        lay.addWidget(self.__widget)
        lay.setContentsMargins(self._margin, self._margin, self._margin, self._margin)
        lay.setSpacing(0)
        self.setLayout(lay)

        if isinstance(self.__menubar, QMenuBar):
            color = self.__menubar.palette().color(QPalette.Base)
            self.__initMenuBar()
        else:
            color = self.__widget.palette().color(QPalette.Base)
        self.setStyleSheet(f'QWidget#titleBar {{ background-color: {color.name()} }}')

    def __initMenuBar(self):
        self.__menubar.installEventFilter(self)
        tool_button = self.__menubar.findChild(QToolButton)
        tool_button.setArrowType(Qt.RightArrow)

    def eventFilter(self, obj, e) -> bool:
        if obj == self:
            # catch resize event or window state change event
            if e.type() == 14 or e.type() == 105:
                self.__toggleNormalOrMaximizedTextByOS()
                # prevent the problem that top title bar window is not visible when full screen turning off
                if e.type() == 105:
                    if int(e.oldState()) == 4:
                        self.__topTitleBar.show()
        # catch full screen toggle event
        if obj.objectName() == 'mainWidget':
            if e.type() == 105:
                self.__toggleFullScreenFromInnerWidget(e)
        # catch the enter event
        if e.type() == 10:
            self.unsetCursor()
            self._resizing = False
        # catch the title change event
        if e.type() == 33:
            self.__titleLbl.setText(obj.windowTitle())
        if obj.objectName() == 'navWidget':
            # catch the menubar double click or mouse move event
            if isinstance(obj, QMenuBar):
                if e.type() == 4 or e.type() == 5:
                    self.__execMenuBarMoveOrDoubleClickEvent(e)
            # catch the titlebar double click or mouse move event
            elif isinstance(obj, TopTitleBarWidget):
                if e.type() == 4 or e.type() == 5:
                    self.__execTitleBarMoveOrDoubleClickEvent(e)
        return super().eventFilter(obj, e)

    def __toggleFullScreenFromInnerWidget(self, e):
        inner_state = int(e.oldState())
        if inner_state == 0 or inner_state == 4:
            if inner_state == 0:
                if isinstance(self.__topTitleBar, TopTitleBarWidget):
                    self.__topTitleBar.hide()
                self.showFullScreen()
            else:
                if isinstance(self.__topTitleBar, TopTitleBarWidget):
                    self.__topTitleBar.show()
                self.showNormal()
            title_bar_state = self.windowState()
            self.__widget.setWindowState(title_bar_state)

    def __execMenuBarMoveOrDoubleClickEvent(self, e):
        p = e.pos()
        if self.__menubar.actionAt(p):
            pass
        else:
            if self.__menubar.activeAction():
                pass
            else:
                # double click (show maximized/normal)
                if e.type() == 4 and e.button() == Qt.LeftButton:
                    self.__showNormalOrMaximizedByOS()
                # move
                else:
                    self._move()

    def __execTitleBarMoveOrDoubleClickEvent(self, e):
        if e.type() == 4 and e.button() == Qt.LeftButton:
            self.__showNormalOrMaximizedByOS()
        else:
            self._move()

    def __showNormalOrMaximizedByOS(self):
        self.__toggleNormalOrMaximizedTextByOS()
        self.__execShowNormalOrMaximized()

    def __toggleNormalOrMaximizedTextByOS(self):
        if self.__styleBasedOnOS == 'windows':
            if self.isMaximized():
                self.__maximizeBtn.setText('🗗')
            else:
                self.__maximizeBtn.setText('🗖')
        elif self.__styleBasedOnOS == 'mac':
            pass

    def __execShowNormalOrMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def setButtonHint(self, hint):
        self.__btnHint = hint

    def setButtonStyle(self, style):
        self.__styleBasedOnOS = style

    def setButtons(self):
        if isinstance(self.__topTitleBar, TopTitleBarWidget):
            self.__topTitleBar.setButtons(self.__btnHint, self.__styleBasedOnOS)
            iconTitleWidget = self.__topTitleBar.getIconTitleWidget()

            self.__btnWidget = self.__topTitleBar.getBtnWidget()
            self.initTitleEvent(iconTitleWidget)
            self.initButtonsEvent()
        else:
            title = self.__widget.windowTitle()
            self.__titleLbl.setText(title)

            lay = QHBoxLayout()
            lay.setContentsMargins(0, 0, 0, 0)

            if self.__styleBasedOnOS == 'windows':
                if isinstance(self.__menubar, QMenuBar):
                    self.__btnWidget = WindowsMinMaxCloseButtonsWidget(self.__menubar, self.__btnHint)
                else:
                    self.__btnWidget = WindowsMinMaxCloseButtonsWidget(self.__widget, self.__btnHint)
            elif self.__styleBasedOnOS == 'mac':
                self.__btnWidget = MacMinMaxCloseButtonsWidget(self.__btnHint)
            self.initButtonsEvent()
            lay.addWidget(self.__btnWidget)

            cornerWidget = QWidget()
            cornerWidget.setLayout(lay)

            # set the corner widget that already exists in QMenuBar
            if self.__menubar:
                existingCornerWidget = self.__menubar.cornerWidget(Qt.TopRightCorner)
                if existingCornerWidget:
                    lay.insertWidget(0, existingCornerWidget)

                # Place the title on appropriate location of QMenuBar
                if len(self.__menubar.actions()) > 0:
                    lay.insertWidget(0, self.__titleLbl, alignment=Qt.AlignLeft)
                else:
                    self.__titleLbl.setContentsMargins(5, 0, 0, 0)
                    self.__menubar.setCornerWidget(self.__titleLbl, Qt.TopLeftCorner)

                self.__menubar.setCornerWidget(cornerWidget, Qt.TopRightCorner)

    def setTopTitleBar(self, title: str = '', icon_filename: str = '', font: QFont = QFont('Arial', 12),
                       align=Qt.AlignCenter, bottom_separator: bool = False):
        if title:
            self.__widget.setWindowTitle(title)
        else:
            title = self.__widget.windowTitle()

        if icon_filename:
            icon_filename = get_absolute_resource_path(icon_filename)
            self.setWindowIcon(QIcon(icon_filename))
        else:
            icon_filename = self.__widget.windowIcon().name()

        if isinstance(self.__menubar, QMenuBar):
            self.__topTitleBar = TopTitleBarWidget(self.__menubar, text=title, font=font, icon_filename=icon_filename,
                                                   align=align)
            self.__menubar.removeEventFilter(self)
        else:
            self.__topTitleBar = TopTitleBarWidget(self.__widget, text=title, font=font, icon_filename=icon_filename,
                                                   align=align)
        self.__topTitleBar.installEventFilter(self)
        self.__topTitleBar.setObjectName('navWidget')
        if bottom_separator:
            self.__topTitleBar.setBottomSeparator()

        lay = self.layout()
        centralWidget = lay.itemAt(0).widget()
        lay.addWidget(self.__topTitleBar, 0, 0, 1, 1)
        lay.addWidget(centralWidget, 1, 0, 1, 1)

        self.setPressToMove(False)

    def getCornerWidget(self):
        return self.__menubar.cornerWidget()

    def initTitleEvent(self, titleWidget):
        self.__windowTitleIconLabel = titleWidget.getSvgLabel()
        self.__titleLbl = titleWidget.getTextLabel()

    def initButtonsEvent(self):
        self.__minimizeBtn = self.__btnWidget.getMinimizedBtn()
        self.__maximizeBtn = self.__btnWidget.getMaximizedBtn()
        self.__closeBtn = self.__btnWidget.getCloseBtn()

        self.__minimizeBtn.clicked.connect(self.showMinimized)
        self.__maximizeBtn.clicked.connect(self.__showNormalOrMaximizedByOS)
        self.__closeBtn.clicked.connect(self.close)

    def getInnerWidget(self):
        return self.__widget