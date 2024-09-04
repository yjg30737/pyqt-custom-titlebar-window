from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMainWindow

from pyqt_custom_titlebar_window.button import Button


class TitlebarButtonsWidget(QWidget):
    def __init__(self, base_widget=None, hint: list = ['min', 'max', 'close']):
        super().__init__()
        self.__initVal(base_widget, hint)
        self.__initUi()

    def __initVal(self, base_widget, hint):
        self._closeBtn = Button(base_widget)
        self._minimizeBtn = Button(base_widget)
        self._maximizeBtn = Button(base_widget)

        self._fullScreenBtn = Button(base_widget)
        self._fullScreenBtn.setStyleAndIcon('ico/full_screen.svg')

        self._helpBtn = Button(base_widget)
        self._helpBtn.setStyleAndIcon('ico/help.svg')

        self._foldBtn = Button(base_widget)
        self._foldBtn.setStyleAndIcon('ico/fold.svg')

        self._fixBtn = Button(base_widget)
        self._fixBtn.setStyleAndIcon('ico/tack.svg')

        self._searchBtn = Button(base_widget)
        self._searchBtn.setStyleAndIcon('ico/search.svg')

        self._btn_dict = {'min': self._minimizeBtn, 'max': self._maximizeBtn, 'close': self._closeBtn,
                          'full_screen': self._fullScreenBtn, 'help': self._helpBtn, 'fold': self._foldBtn,
                          'fix': self._fixBtn}

        self._base_widget = base_widget
        self.__window = self._base_widget.window()
        self.__window.installEventFilter(self)
        self._hint = hint

    def __initUi(self):
        lay = QHBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        for k in self._hint:
            # hint str
            if k in self._btn_dict:
                lay.addWidget(self._btn_dict[k])
            # widget
            else:
                lay.addWidget(k)

        self.setLayout(lay)

        self._styleInit()

        # raise - helps the button widget not to be blocked by something else
        self.raise_()

    def _styleInit(self):
        # fill the button's background with color
        if isinstance(self._base_widget, QMainWindow):
            palette = self._base_widget.menuBar().palette()
        else:
            palette = self._base_widget.palette()
        background_color = palette.color(QPalette.Base).name()
        for btn in self._btn_dict.values():
            btn.setBackground(background_color)

    def event(self, e):
        if e.type() == 100:
            self._styleInit()
        return super().event(e)

    def setMinimizedBtn(self, btn):
        self._minimizeBtn = btn

    def setMaximizedBtn(self, btn):
        self._maximizeBtn = btn

    def setCloseBtn(self, btn):
        self._closeBtn = btn

    def setFullScreenBtn(self,  btn):
        self._fullScreenBtn = btn

    def setFixBtn(self, btn):
        self._fixBtn = btn

    def setFoldBtn(self, btn):
        self._foldBtn = btn

    def setHelpBtn(self, btn):
        self._helpBtn = btn

    def getMinimizedBtn(self):
        return self._minimizeBtn

    def getMaximizedBtn(self):
        return self._maximizeBtn

    def getCloseBtn(self):
        return self._closeBtn

    def getFullScreenBtn(self):
        return self._fullScreenBtn

    def getFixBtn(self):
        return self._fixBtn

    def getFoldBtn(self):
        return self._foldBtn

    def getHelpBtn(self):
        return self._helpBtn

    def setButtonIcon(self, hint: str, icon_filename: str):
        self._btn_dict[hint].setIcon(icon_filename)

    def setButtonSize(self, w, h):
        w = int(w)
        h = int(h)
        for k, v in self._btn_dict.items():
            if v.text():
                f = v.font()
                f.setPointSize(max(11, min(5, w // 2)))
                v.setFont(f)
            elif v.icon():
                v.setIconSize(QSize(w, h))
            v.setFixedSize(int(w*1.25), h)