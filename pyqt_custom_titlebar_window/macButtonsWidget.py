from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import qApp

from pyqt_custom_titlebar_window.titlebarButtonsWidget import TitlebarButtonsWidget


class MacButtonsWidget(TitlebarButtonsWidget):
    def __init__(self, base_widget=None, hint=['min', 'max', 'close']):
        super().__init__(base_widget, hint)
        self.__size = qApp.font().pointSize()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__border_width = self.__size // 20
        self.__border_radius = self.__size // 2
        self.__macBtnStyle = ''

    def __initUi(self):
        self.layout().setSpacing(2)
        btns = [self._closeBtn, self._minimizeBtn, self._maximizeBtn]
        colors = ['#DD0000', '#AA8800', '#008800']
        for i in range(len(btns)):
            btn = btns[i]
            btn.setFixedSize(self.__size, self.__size)
            self.__setStyleForEachButton(btn, colors[i])

    def _styleInit(self):
        pass

    def __setStyleForEachButton(self, btn, color):
        border_color = QColor(color)
        border_color_name = border_color.name()
        background_color_name = border_color.lighter().name()

        self.__macBtnStyle = f'''
                             QPushButton
                             {{ 
                             background-color: {background_color_name};
                             border: {self.__border_width} solid {border_color_name};
                             border-radius: {self.__border_radius};
                             }}
                             '''

        btn.setStyleSheet(self.__macBtnStyle)

    def setButtonSize(self, w, h):
        self.__size = w
        self.__initVal()
        btns = [self._closeBtn, self._minimizeBtn, self._maximizeBtn]
        colors = ['#DD0000', '#AA8800', '#008800']
        for i in range(len(btns)):
            btn = btns[i]
            btn.setFixedSize(self.__size, self.__size)
            self.__setStyleForEachButton(btn, colors[i])