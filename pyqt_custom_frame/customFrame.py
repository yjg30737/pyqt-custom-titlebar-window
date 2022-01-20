from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPalette
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QMainWindow, QToolButton, qApp


class CustomFrame(QWidget):
    def __init__(self, main_window: QMainWindow):
        super().__init__()
        self.__resized = False

        self.__margin = 3
        self.__cursor = QCursor()

        self.__initPosition()
        self.__initUi(main_window)

    def __initUi(self, main_window):
        self.setMinimumSize(60, 60)
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.__mainWindow = main_window
        self.__mainWindow.enterEvent = self.enterTheMainWindowEvent

        self.__menuBar = self.__mainWindow.menuBar()
        self.__menuBar.installEventFilter(self)

        lay = QGridLayout()
        lay.addWidget(self.__mainWindow)
        lay.setContentsMargins(self.__margin, self.__margin, self.__margin, self.__margin)
        self.setLayout(lay)

    def __initPosition(self):
        self.__top = False
        self.__bottom = False
        self.__left = False
        self.__right = False

    def __setCursorShapeForCurrentPoint(self, p):
        rect = self.rect()
        rect.setX(self.rect().x() + self.__margin)
        rect.setY(self.rect().y() + self.__margin)
        rect.setWidth(self.rect().width() - self.__margin * 2)
        rect.setHeight(self.rect().height() - self.__margin * 2)

        self.__resized = rect.contains(p)
        if self.__resized:

            # cursor inside of widget
            self.unsetCursor()
            self.__cursor = self.cursor()
            self.__initPosition()
        else:
            # resize
            x = p.x()
            y = p.y()

            x1 = self.rect().x()
            y1 = self.rect().y()
            x2 = self.rect().width()
            y2 = self.rect().height()

            self.__left = abs(x - x1) <= self.__margin
            self.__top = abs(y - y1) <= self.__margin
            self.__right = abs(x - (x2 + x1)) <= self.__margin
            self.__bottom = abs(y - (y2 + y1)) <= self.__margin

            if self.__top and self.__left:
                self.__cursor.setShape(Qt.SizeFDiagCursor)
            elif self.__top and self.__right:
                self.__cursor.setShape(Qt.SizeBDiagCursor)
            elif self.__bottom and self.__left:
                self.__cursor.setShape(Qt.SizeBDiagCursor)
            elif self.__bottom and self.__right:
                self.__cursor.setShape(Qt.SizeFDiagCursor)
            elif self.__left:
                self.__cursor.setShape(Qt.SizeHorCursor)
            elif self.__top:
                self.__cursor.setShape(Qt.SizeVerCursor)
            elif self.__right:
                self.__cursor.setShape(Qt.SizeHorCursor)
            elif self.__bottom:
                self.__cursor.setShape(Qt.SizeVerCursor)
            self.setCursor(self.__cursor)

        self.__resized = not self.__resized

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__resize()
        return super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        self.__setCursorShapeForCurrentPoint(e.pos())
        return super().mouseMoveEvent(e)

    def enterEvent(self, e):
        self.__setCursorShapeForCurrentPoint(e.pos())
        return super().enterEvent(e)

    def __resize(self):
        window = self.windowHandle()
        if self.__resized:
            if self.__cursor.shape() == Qt.SizeHorCursor:
                if self.__left:
                    window.startSystemResize(Qt.LeftEdge)
                elif self.__right:
                    window.startSystemResize(Qt.RightEdge)
            elif self.__cursor.shape() == Qt.SizeVerCursor:
                if self.__top:
                    window.startSystemResize(Qt.TopEdge)
                elif self.__bottom:
                    window.startSystemResize(Qt.BottomEdge)
            elif self.__cursor.shape() == Qt.SizeBDiagCursor:
                if self.__top and self.__right:
                    window.startSystemResize(Qt.TopEdge | Qt.RightEdge)
                elif self.__bottom and self.__left:
                    window.startSystemResize(Qt.BottomEdge | Qt.LeftEdge)
            elif self.__cursor.shape() == Qt.SizeFDiagCursor:
                if self.__top and self.__left:
                    window.startSystemResize(Qt.TopEdge | Qt.LeftEdge)
                elif self.__bottom and self.__right:
                    window.startSystemResize(Qt.BottomEdge | Qt.RightEdge)

    def __move(self):
        window = self.windowHandle()
        if self.__resized:
            pass
        else:
            window.startSystemMove()

    def enterTheMainWindowEvent(self, e):
        self.unsetCursor()
        self.__resized = False
        return super().enterEvent(e)

    def eventFilter(self, obj, e) -> bool:
        # double click or move event
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
                    self.__move()

    def __showNormalOrMaximized(self):
        if self.isMaximized():
            self.__maximizeBtn.setText('🗖')
            self.showNormal()
        else:
            self.__maximizeBtn.setText('🗗')
            self.showMaximized()

    def setMinMaxCloseButton(self):
        minimizeBtn = QToolButton()
        minimizeBtn.setText('🗕')
        minimizeBtn.clicked.connect(self.showMinimized)

        self.__maximizeBtn = QToolButton()
        self.__maximizeBtn.setText('🗖')
        self.__maximizeBtn.clicked.connect(self.__showNormalOrMaximized)

        closeBtn = QToolButton()
        closeBtn.setText('🗙')
        closeBtn.clicked.connect(self.close)

        btns = [minimizeBtn, self.__maximizeBtn, closeBtn]

        menubar_base_color = self.__menuBar.palette().color(QPalette.Base)
        menubar_base_color = menubar_base_color.darker(300)
        tool_button_style = f'QToolButton ' \
                            f'{{ background: transparent; border: 0; }} ' \
                            f'QToolButton:hover ' \
                            f'{{ background-color: {menubar_base_color.name()}; }}'

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

        cornerWidget = QWidget()
        cornerWidget.setLayout(lay)

        self.__menuBar.setCornerWidget(cornerWidget, Qt.TopRightCorner)