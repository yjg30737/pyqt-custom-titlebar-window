from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QFont, QIcon
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QMainWindow, QPushButton, QLabel, \
    QMenuBar, QToolButton, qApp, QSizePolicy

from pyqt_frameless_window.framelessWindow import FramelessWindow

from pyqt_top_titlebar_widget import TopTitleBarWidget

from pyqt_svg_label import SvgLabel

from pyqt_windows_buttons_widget import WindowsButtonsWidget
from pyqt_mac_buttons_widget import MacButtonsWidget
from pyqt_resource_helper import PyQtResourceHelper
import absresgetter


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
        self.__iconLbl = QLabel()

        self.__topTitleBar = QWidget()
        self.__btnWidget = QWidget()
        self.__btnHint = ['min', 'max', 'close']

        self.__minimizeBtn = QPushButton()
        self.__maximizeBtn = QPushButton()
        self.__closeBtn = QPushButton()

        self.__style = qApp.platformName()
        if self.__style == 'windows' or self.__style == 'mac':
            pass
        else:
            self.__style = 'windows'

    def __initUi(self):
        self.__widget.installEventFilter(self)
        self.installEventFilter(self)

        # connect the close event with inner widget
        self.closeEvent = self.__widget.closeEvent

        lay = QGridLayout()
        lay.addWidget(self.__widget)
        lay.setContentsMargins(self._margin, self._margin, self._margin, self._margin)
        lay.setSpacing(self._margin)
        self.setLayout(lay)

        self.__modernizeAppFont()

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

    # modernize the application
    def __modernizeAppFont(self):
        # modernize the font
        appFont = qApp.font()
        # font family: arial
        appFont.setFamily('Arial')
        # font size: 9~12
        appFont.setPointSize(min(12, max(9, appFont.pointSize() * qApp.desktop().logicalDotsPerInch()/96.0)))
        # font style strategy: antialiasing
        appFont.setStyleStrategy(QFont.PreferAntialias)
        qApp.setFont(appFont)
        # fade menu and tooltip
        qApp.setEffectEnabled(Qt.UI_FadeMenu, True)
        qApp.setEffectEnabled(Qt.UI_FadeTooltip, True)

    def eventFilter(self, obj, e) -> bool:
        if obj == self:
            # catch resize event or window state change event
            if e.type() == 14 or e.type() == 105:
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
                elif e.type() == 100:
                    cornerWidget = self.getCornerWidget()
                    if cornerWidget:
                        # apply background color change to corner widget and title label
                        color = self.__menubar.palette().color(QPalette.Base)
                        cornerWidget.setStyleSheet(f'QWidget {{ background-color: {color.name()} }};')
                        self.__titleLbl.setStyleSheet(f'QWidget {{ background-color: {color.name()} }};')

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
        self.__execShowNormalOrMaximized()

    def __execShowNormalOrMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def setButtonHint(self, hint):
        self.__btnHint = hint

    def __getProperButtonsWidget(self, widget, btnWidget=None):
        if btnWidget:
            pass
        else:
            if self.__style == 'windows':
                btnWidget = WindowsButtonsWidget(widget, self.__btnHint)
            elif self.__style == 'mac':
                btnWidget = MacButtonsWidget(widget, self.__btnHint)
        return btnWidget

    # btnWidget(user-customized button widget), currently being developed
    def setButtons(self, btnWidget=None, align=Qt.AlignRight):
        # If window has a TopTitleBarWidget
        if isinstance(self.__topTitleBar, TopTitleBarWidget):
            self.__btnWidget = self.__getProperButtonsWidget(self.__topTitleBar, btnWidget)

            # set proper align value based on type of buttons widget (temporary code)
            # fixme start
            if isinstance(self.__btnWidget, WindowsButtonsWidget):
                align = Qt.AlignRight
            elif isinstance(self.__btnWidget, MacButtonsWidget):
                align = Qt.AlignLeft
            # end

            self.__topTitleBar.setButtons(self.__btnWidget, align)
            iconTitleWidget = self.__topTitleBar.getIconTitleWidget()
            self.initTitleEvent(iconTitleWidget)
            self.initButtonsEvent()
        # If window has only a menu bar
        else:
            lay = QHBoxLayout()
            lay.setContentsMargins(0, 0, 0, 0)
            self.__btnWidget = self.__getProperButtonsWidget(self.__menubar, btnWidget)
            self.initButtonsEvent()
            lay.addWidget(self.__btnWidget)

            cornerWidget = QWidget()
            cornerWidget.setLayout(lay)
            # set the corner widget that already exists in QMenuBar
            if self.__menubar:
                existingCornerWidget = self.__menubar.cornerWidget(Qt.TopRightCorner)
                if existingCornerWidget:
                    lay.insertWidget(0, existingCornerWidget)
                    if self.__titleLbl.text():
                        lay.insertWidget(0, self.__titleLbl)

                cornerWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
                cornerWidget.setMinimumHeight(self.__menubar.height())

                self.__menubar.setCornerWidget(cornerWidget, Qt.TopRightCorner)

    def __getWindowTitle(self, title):
        if title:
            pass
        else:
            title = self.__widget.windowTitle()
        return title

    def __getWindowIcon(self, icon_filename):
        if icon_filename:
            icon_filename = absresgetter.getabsres(icon_filename)
        else:
            icon_filename = self.__widget.windowIcon().name()
        return icon_filename

    def __setWindowIcon(self, icon_filename):
        icon_filename = self.__getWindowIcon(icon_filename)
        self.setWindowIcon(QIcon(icon_filename))

    def setMenuTitle(self, title: str = '', icon_filename: str = '', font: QFont = QFont('Arial', 9)):
        # set menu title
        title = self.__getWindowTitle(title)
        self.__titleLbl.setText(title)
        self.__titleLbl.setFont(font)
        self.__titleLbl.setMinimumHeight(self.__menubar.height())
        cornerWidget = self.__menubar.cornerWidget()
        if cornerWidget:
            lay = cornerWidget.layout()
            if lay:
                lay.insertWidget(0, self.__titleLbl)
        else:
            self.__menubar.setCornerWidget(self.__titleLbl, Qt.TopRightCorner)
        self.setWindowTitle(title)

        # set menu icon
        self.__iconLbl = SvgLabel()
        self.__iconLbl.setSvgFile(icon_filename)
        self.__iconLbl.setFixedSize(self.__menubar.sizeHint().height() // 1.2, self.__menubar.sizeHint().height() // 1.2)
        self.__menubar.setCornerWidget(self.__iconLbl, Qt.TopLeftCorner)
        self.__setWindowIcon(icon_filename)

    def setTopTitleBar(self, title: str = '', icon_filename: str = '', font: QFont = QFont('Arial', 14),
                       align=Qt.AlignCenter, bottom_separator: bool = False):
        title = self.__getWindowTitle(title)
        self.__setWindowIcon(icon_filename)

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

        # Set app title
        self.setWindowTitle(title)

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
        self.__maximizeBtn.clicked.connect(self.__showNormalOrMaximized)
        self.__closeBtn.clicked.connect(self.close)

    def getInnerWidget(self):
        return self.__widget